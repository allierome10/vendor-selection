#!/usr/bin/env python3
"""
scoring_engine.py — Bias-free comparative scoring for platform/vendor assessments.

Combines two methods so rankings are defensible rather than impressionistic:

  1. Elo tournament (per criterion): every option plays every other option
     head-to-head on each criterion. Match outcomes come from the analyst's
     pairwise judgment (which option better satisfies THIS criterion, given the
     client requirements), NOT from a flat Low/Med/High label. Ratings converge
     to a stable ordinal+interval ranking and expose intransitive (inconsistent)
     judgments.

  2. Monte Carlo (uncertainty bands): each pairwise judgment carries a
     confidence. We resample outcomes thousands of times within that confidence
     to produce a distribution of final scores per option, yielding a mean,
     a 90% credible interval, and P(rank 1).

INPUT: a JSON file describing criteria (with client-derived weights), options,
and pairwise judgments. See build_input_template() for the schema.

OUTPUT: a JSON results object with per-criterion Elo, weighted composite,
Monte Carlo bands, pairwise consistency diagnostics, and a final numeric stack
ranking. Nothing in here knows or cares who the vendor is — see the bias rules
in SKILL.md. Identity must never enter a pairwise judgment.

Usage:
    python3 scoring_engine.py --input assessment_input.json --output results.json
    python3 scoring_engine.py --template            # prints the input schema
"""

import argparse
import itertools
import json
import math
import random
from collections import defaultdict

K_FACTOR = 24            # Elo update step; moderate so single matches don't dominate
ELO_BASE = 1500.0        # starting rating for every option (identical start = no prior bias)
ELO_ROUNDS = 40          # tournament passes; ratings stabilize well before this
MC_TRIALS = 10000        # Monte Carlo resamples
RANDOM_SEED = 7          # fixed for reproducibility; document it in the report


# --------------------------------------------------------------------------- #
# Input schema
# --------------------------------------------------------------------------- #
def build_input_template():
    """Return an annotated example of the expected input JSON."""
    return {
        "decision": "Platform A vs Platform B for enterprise CRM agent layer",
        "options": ["Platform A", "Platform B", "Platform C"],
        "criteria": [
            {
                "name": "Ecosystem fit",
                # Weight is client-derived (from intake / requirements). Weights
                # across criteria should sum to ~1.0 but are normalized anyway.
                "weight": 0.25,
                # Pairwise judgments: for each unordered pair, who wins on THIS
                # criterion and how decisively. score is P(row beats col), 0..1.
                #   0.5  = a genuine tie
                #   0.65 = mild edge
                #   0.8  = clear edge
                #   0.95 = decisive
                # confidence 0..1 = how sure the analyst is in this judgment
                # (drives Monte Carlo band width). Low evidence => low confidence,
                # NOT a guessed midpoint.
                "pairwise": [
                    {"a": "Platform A", "b": "Platform B", "score": 0.65, "confidence": 0.7,
                     "rationale": "A integrates natively with the client's existing identity + data catalog; B requires a connector layer."},
                    {"a": "Platform A", "b": "Platform C", "score": 0.80, "confidence": 0.8,
                     "rationale": "..."},
                    {"a": "Platform B", "b": "Platform C", "score": 0.60, "confidence": 0.5,
                     "rationale": "..."}
                ]
            }
        ]
    }


# --------------------------------------------------------------------------- #
# Elo
# --------------------------------------------------------------------------- #
def _expected(r_a, r_b):
    return 1.0 / (1.0 + 10 ** ((r_b - r_a) / 400.0))


def run_elo_for_criterion(options, pairwise):
    """Run a round-robin Elo tournament for one criterion.

    pairwise: list of {a,b,score} where score = P(a beats b), 0..1.
    Returns dict option -> rating.
    """
    ratings = {o: ELO_BASE for o in options}
    # index judgments by unordered pair
    lookup = {}
    for p in pairwise:
        lookup[(p["a"], p["b"])] = p["score"]
        lookup[(p["b"], p["a"])] = 1.0 - p["score"]

    pairs = list(itertools.permutations(options, 2))
    rng = random.Random(RANDOM_SEED)
    for _ in range(ELO_ROUNDS):
        rng.shuffle(pairs)
        for a, b in pairs:
            if (a, b) not in lookup:
                continue
            actual = lookup[(a, b)]          # outcome in [0,1]
            exp_a = _expected(ratings[a], ratings[b])
            ratings[a] += K_FACTOR * (actual - exp_a)
            ratings[b] += K_FACTOR * ((1 - actual) - (1 - exp_a))
    return ratings


def elo_to_unit(ratings):
    """Normalize a rating dict to 0..1 (min-max) for cross-criterion blending."""
    vals = list(ratings.values())
    lo, hi = min(vals), max(vals)
    if math.isclose(hi, lo):
        return {k: 0.5 for k in ratings}
    return {k: (v - lo) / (hi - lo) for k, v in ratings.items()}


# --------------------------------------------------------------------------- #
# Consistency diagnostics (transitivity)
# --------------------------------------------------------------------------- #
def consistency_report(options, pairwise):
    """Detect intransitive triples: A>B, B>C, but C>A. Flags shaky judgments."""
    win = {}
    for p in pairwise:
        win[(p["a"], p["b"])] = p["score"] >= 0.5
        win[(p["b"], p["a"])] = p["score"] < 0.5
    violations = []
    for a, b, c in itertools.permutations(options, 3):
        if (a, b) in win and (b, c) in win and (c, a) in win:
            if win[(a, b)] and win[(b, c)] and win[(c, a)]:
                violations.append([a, b, c])
    # dedupe cyclic rotations
    seen, uniq = set(), []
    for v in violations:
        key = frozenset(v)
        if key not in seen:
            seen.add(key)
            uniq.append(v)
    n_pairs = len(list(itertools.combinations(options, 2)))
    return {
        "intransitive_triples": uniq,
        "n_pairwise_judgments": len(pairwise),
        "n_possible_pairs": n_pairs,
        "coverage": round(len(pairwise) / n_pairs, 3) if n_pairs else 1.0,
    }


# --------------------------------------------------------------------------- #
# Monte Carlo
# --------------------------------------------------------------------------- #
def run_monte_carlo(options, criteria, weights):
    """Resample pairwise outcomes within their confidence to get score bands.

    For each trial we perturb every pairwise 'score' by noise scaled to
    (1 - confidence), rerun Elo per criterion, blend by weight, and record the
    composite. Returns per-option distribution stats.
    """
    rng = random.Random(RANDOM_SEED)
    samples = defaultdict(list)
    rank1 = defaultdict(int)

    for _ in range(MC_TRIALS):
        composite = {o: 0.0 for o in options}
        for crit in criteria:
            w = weights[crit["name"]]
            perturbed = []
            for p in crit["pairwise"]:
                conf = max(0.01, min(1.0, p.get("confidence", 0.6)))
                sigma = (1 - conf) * 0.25      # max ~0.25 std at zero confidence
                noisy = p["score"] + rng.gauss(0, sigma)
                noisy = max(0.02, min(0.98, noisy))
                perturbed.append({"a": p["a"], "b": p["b"], "score": noisy})
            ratings = run_elo_for_criterion(options, perturbed)
            unit = elo_to_unit(ratings)
            for o in options:
                composite[o] += w * unit[o]
        # record
        for o in options:
            samples[o].append(composite[o])
        winner = max(composite, key=composite.get)
        rank1[winner] += 1

    stats = {}
    for o in options:
        s = sorted(samples[o])
        n = len(s)
        mean = sum(s) / n
        lo = s[int(0.05 * n)]
        hi = s[int(0.95 * n) - 1]
        stats[o] = {
            "mean": round(mean, 4),
            "ci90_low": round(lo, 4),
            "ci90_high": round(hi, 4),
            "p_rank1": round(rank1[o] / MC_TRIALS, 4),
        }
    return stats


# --------------------------------------------------------------------------- #
# Orchestration
# --------------------------------------------------------------------------- #
def assess(payload):
    options = payload["options"]
    criteria = payload["criteria"]

    # normalize weights
    total_w = sum(c["weight"] for c in criteria)
    weights = {c["name"]: c["weight"] / total_w for c in criteria}

    per_criterion = {}
    composite = {o: 0.0 for o in options}
    diagnostics = {}

    for crit in criteria:
        ratings = run_elo_for_criterion(options, crit["pairwise"])
        unit = elo_to_unit(ratings)
        per_criterion[crit["name"]] = {
            "weight": round(weights[crit["name"]], 4),
            "elo": {k: round(v, 1) for k, v in ratings.items()},
            "normalized_0_1": {k: round(v, 4) for k, v in unit.items()},
        }
        for o in options:
            composite[o] += weights[crit["name"]] * unit[o]
        diagnostics[crit["name"]] = consistency_report(options, crit["pairwise"])

    mc = run_monte_carlo(options, criteria, weights)

    # final numeric stack ranking on 0..100 scale
    ranking = sorted(options, key=lambda o: composite[o], reverse=True)
    final = []
    for rank, o in enumerate(ranking, 1):
        final.append({
            "rank": rank,
            "option": o,
            "score_0_100": round(composite[o] * 100, 1),
            "mc_mean_0_100": round(mc[o]["mean"] * 100, 1),
            "mc_ci90_0_100": [round(mc[o]["ci90_low"] * 100, 1),
                              round(mc[o]["ci90_high"] * 100, 1)],
            "p_rank1": mc[o]["p_rank1"],
        })

    return {
        "decision": payload.get("decision", ""),
        "method": "Elo round-robin per criterion + Monte Carlo confidence bands",
        "seed": RANDOM_SEED,
        "mc_trials": MC_TRIALS,
        "final_stack_ranking": final,
        "per_criterion": per_criterion,
        "consistency_diagnostics": diagnostics,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input")
    ap.add_argument("--output")
    ap.add_argument("--template", action="store_true")
    args = ap.parse_args()

    if args.template:
        print(json.dumps(build_input_template(), indent=2))
        return

    with open(args.input) as f:
        payload = json.load(f)
    results = assess(payload)
    out = json.dumps(results, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
