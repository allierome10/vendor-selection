#!/usr/bin/env python3
"""
cost_estimator.py — Volumetric cost model for the AI ecosystem layers.

Built around the reference volumetric structure in
reference/volumetric_components.csv (the "AI Economics at Scale" mini-RFP):
five layers — OS/Workbench, Agent, Model, Data Foundation (Platform),
Data Foundation (Infra) — each with cost components, units, and baseline +
3-year scaled volumes.

This script does NOT ship hard-coded vendor prices. Unit prices must be
supplied at runtime from (a) client-provided pricing, or (b) live web-search
of hyperscaler public pricing calculators (see SKILL.md cost workflow). You
pass a prices JSON mapping each component to a unit price; the script scales
volumes to the client's profile, applies an environment multiplier
(Dev/Test/Prod), a FinOps adjustment, and returns monthly + annual cost by
layer and component, with a low/expected/high band.

Usage:
    # 1. dump the component skeleton (volumes prefilled from reference)
    python3 cost_estimator.py --skeleton --reference reference/volumetric_components.csv > prices.json
    # 2. fill in unit_price (+ optional volume overrides) in prices.json
    # 3. estimate
    python3 cost_estimator.py --prices prices.json --output cost_results.json \
        --scale-profile mid --environments 3 --finops-adjustment 0.9
"""

import argparse
import csv
import json


# Scale profile selects which reference volume column to anchor on, then lets
# the analyst override per-component for client specifics.
SCALE_PROFILES = {
    "baseline": "baseline_volume",          # today / pilot
    "mid": "interpolate",                    # halfway to full adoption
    "full": "projected_volume",              # 3-year full enterprise adoption
}


def load_reference(path):
    comps = []
    with open(path, newline="") as f:
        r = csv.DictReader(f)
        # normalize header names
        for row in r:
            try:
                base = float(row.get("Baseline Volume") or 0)
            except ValueError:
                base = 0.0
            try:
                proj = float(row.get("3-year Out Projected Volume at Scale (Full Ent. Adoption)") or 0)
            except ValueError:
                proj = 0.0
            comps.append({
                "layer": row["Layer"].strip(),
                "component": row["Cost Component"].strip(),
                "unit": (row.get("Unit") or "").strip(),
                "baseline_volume": base,
                "projected_volume": proj,
                "assumption": (row.get("3-Year Scale Assumptions (Full Ent. Adoption)") or "").strip(),
            })
    return comps


def emit_skeleton(reference_path):
    """Produce a prices.json the analyst fills in with unit prices + overrides."""
    comps = load_reference(reference_path)
    skel = {
        "currency": "USD",
        "pricing_source": "FILL ME: client-provided | hyperscaler public calculator (cite URL + date)",
        "components": []
    }
    for c in comps:
        skel["components"].append({
            "layer": c["layer"],
            "component": c["component"],
            "unit": c["unit"],
            "baseline_volume": c["baseline_volume"],
            "projected_volume": c["projected_volume"],
            "volume_override": None,         # set to a number to override scale logic
            "unit_price": None,              # REQUIRED: price per unit per month
            "price_note": ""                 # cite source / SKU / calculator inputs
        })
    return skel


def resolve_volume(c, profile):
    if c.get("volume_override") is not None:
        return float(c["volume_override"])
    key = SCALE_PROFILES.get(profile, "baseline_volume")
    if key == "interpolate":
        return (float(c["baseline_volume"]) + float(c["projected_volume"])) / 2.0
    return float(c[key])


def estimate(prices, profile, environments, finops_adjustment):
    """Return monthly + annual cost rolled up by layer and component."""
    by_layer = {}
    grand_monthly = 0.0
    missing_prices = []

    for c in prices["components"]:
        up = c.get("unit_price")
        if up is None:
            missing_prices.append(f"{c['layer']} / {c['component']}")
            continue
        vol = resolve_volume(c, profile)
        # environment multiplier: Dev+Test+Prod. Test is heaviest; model the
        # combined multiple as ~ environments (analyst can refine per component).
        env_mult = float(environments)
        raw_monthly = vol * float(up) * env_mult
        adj_monthly = raw_monthly * float(finops_adjustment)
        by_layer.setdefault(c["layer"], {"components": [], "monthly": 0.0})
        by_layer[c["layer"]]["components"].append({
            "component": c["component"],
            "unit": c["unit"],
            "volume": vol,
            "unit_price": up,
            "env_multiplier": env_mult,
            "monthly_cost": round(adj_monthly, 2),
        })
        by_layer[c["layer"]]["monthly"] += adj_monthly
        grand_monthly += adj_monthly

    # uncertainty band: pricing + volume estimation error
    low = grand_monthly * 0.85
    high = grand_monthly * 1.25     # asymmetric: overruns more common than savings

    layer_summary = []
    for layer, d in by_layer.items():
        layer_summary.append({
            "layer": layer,
            "monthly_cost": round(d["monthly"], 2),
            "annual_cost": round(d["monthly"] * 12, 2),
            "share_of_total": round(d["monthly"] / grand_monthly, 4) if grand_monthly else 0,
            "components": sorted(d["components"], key=lambda x: -x["monthly_cost"]),
        })
    layer_summary.sort(key=lambda x: -x["monthly_cost"])

    return {
        "currency": prices.get("currency", "USD"),
        "pricing_source": prices.get("pricing_source", ""),
        "scale_profile": profile,
        "environments_counted": environments,
        "finops_adjustment": finops_adjustment,
        "total_monthly_cost": round(grand_monthly, 2),
        "total_annual_cost": round(grand_monthly * 12, 2),
        "annual_band_expected_low_high": [round(low * 12, 2),
                                          round(grand_monthly * 12, 2),
                                          round(high * 12, 2)],
        "by_layer": layer_summary,
        "components_missing_price": missing_prices,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skeleton", action="store_true")
    ap.add_argument("--reference", default="reference/volumetric_components.csv")
    ap.add_argument("--prices")
    ap.add_argument("--output")
    ap.add_argument("--scale-profile", default="mid", choices=list(SCALE_PROFILES))
    ap.add_argument("--environments", type=int, default=3)
    ap.add_argument("--finops-adjustment", type=float, default=1.0,
                    help="multiplier for committed-use/reserved discounts, e.g. 0.9 = 10% off")
    args = ap.parse_args()

    if args.skeleton:
        print(json.dumps(emit_skeleton(args.reference), indent=2))
        return

    with open(args.prices) as f:
        prices = json.load(f)
    results = estimate(prices, args.scale_profile, args.environments, args.finops_adjustment)
    out = json.dumps(results, indent=2)
    if args.output:
        with open(args.output, "w") as f:
            f.write(out)
        print(f"Wrote {args.output}")
    else:
        print(out)


if __name__ == "__main__":
    main()
