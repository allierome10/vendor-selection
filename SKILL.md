---
name: platform-comparison-assessment
description: >
  Structured enterprise technology decision assessments for strategy, architecture, and vendor/platform evaluation.
  Use this skill whenever the user wants to evaluate a technology option, compare platforms or vendors, decide between build/buy/hybrid approaches,
  assess integration fit, determine if a POC is needed, size the cost of an AI/data platform estate, or make any structured technology
  decision grounded in business value and ecosystem fit.
  Trigger on phrases like "should we use X", "compare A vs B", "evaluate this vendor", "assess this platform", "is this a good fit",
  "build or buy", "do we need a POC", "technology decision", "architecture decision", "vendor assessment", "RFP/RFQ scoring",
  "cost/TCO of an AI platform", or any request for a structured technology recommendation. Also trigger when the user describes a
  business problem and mentions specific technology options, even if they don't use the word "assess" or "evaluate".
  This skill applies the Deloitte-style three-stage framework: Clarify Value → Assess Fit → Validate & Decide,
  scored with a bias-free Elo + Monte Carlo engine and an optional volumetric cost model.
---

# Technology Decision Assessment Skill

## Purpose

Turn ambiguous enterprise technology questions into clear, decision-ready assessments. The output is executive-friendly, analytically rigorous, grounded in business value (not feature lists), scored scientifically rather than by gut-feel labels, and accompanied by client-ready deliverables typical of a week-1 consulting engagement.

---

## START HERE: The Launch Pad

**Every invocation begins at the launch pad.** Before doing any analysis, present the launch pad as an interactive choose-your-own-journey so the user sets the path. Render this as the elicitation widget (see "Launch Pad UX" below). It captures two things:

### 1. Intake mode
- **Free response** — the user describes the situation in their own words; you parse it into the framework and only ask for what's genuinely missing.
- **Guided intake** — you walk the user through the structured intake questionnaire (see "Guided Intake" below). Default for users who want help scoping.
- **Mixed free / guided intake** — mostly guided, but leaning on free response. Use the structured intake questionnaire as the backbone, but invite the user to answer in their own words and elaborate freely; parse those open answers into the framework and only formally pose the guided questions that remain genuinely unanswered. A middle path for users who want the structure of the questionnaire without a rigid, one-question-at-a-time interrogation.

### 2. Available information
- **Client documents available** — request and ingest whatever the client/user has: business requirement docs, technical requirement docs, current tech-stack inventory, consumption/commitment agreements, architecture diagrams, data estate descriptions, roadmaps. The more provided, the higher the confidence and the more client-specific the grading.
- **No client documents** — proceed on **publicly available information via web search only**, paired with the reference material in this skill's backend (`reference/`). Be explicit in the output that grading rests on public info + assumptions, and that confidence is correspondingly lower. This is exactly the gap the Data Gathering Request document (below) is designed to close.

Do not start scoring until the user has chosen a journey. If they ignore the launch pad and just start describing a problem, infer their choices, state what you inferred, and proceed.

---

## Guided Intake

When the user picks guided intake (or when free-response leaves key gaps), ask the following, **one screen at a time**, using the elicitation widget with tappable options where possible and free-text where the answer is open. Pre-fill / skip any item already known from uploaded docs or the conversation. Keep it moving — this is scoping, not an interrogation.

Ask in this order:

1. **Client industry** — what industry is the client in? (e.g., Financial Services, Healthcare, Retail/CPG, Manufacturing, Public Sector, Tech, Energy.)
2. **Requesting stakeholder** — which client stakeholder is requesting this assessment? (e.g., CIO, CTO, COO, CDO, CFO, Chief AI Officer, Head of Architecture, business-unit lead.) This shapes tone, emphasis, and which gating criteria carry weight.
3. **Platforms / agents in scope** — is there a specific platform(s) or agent(s) to assess or compare? Capture the named options, or "open — recommend candidates."
4. **Current tech estate** — what is the estate like? Probe for: tech debt level, centralized vs. fragmented architecture, ERP-centric vs. best-of-breed / domain-specific platforms, structured vs. unstructured data balance, integration maturity.
5. **Cloud / hyperscaler** — which hyperscaler(s) do they use? (AWS, Azure, GCP, OCI, multi-cloud, on-prem-heavy.)
6. **Consumption commitments** — are there committed-use / reserved / EDP-type spend commitments in place with that hyperscaler? And is the deployment **on-prem vs. off-prem (cloud)** — or hybrid? (Commitments drive the FinOps adjustment in the cost model.)
7. **Domain being assessed** — which functional/data domain? (e.g., CRM, Supply Chain, Warehouse, Transportation, CPQ, Chart of Accounts / Finance, HR, Procurement, Customer Service.)
8. **Value proposition to assess** — is there a specific value proposition or hypothesis to evaluate on the client's behalf? (e.g., "consolidate three agent platforms onto one," "cut model inference cost 30%," "stand up a CRM agent in one quarter.")

After intake, restate the captured profile back to the user in 6–10 lines and confirm before proceeding. This profile drives criteria weighting, cost scaling, and the data-gathering request.

---

## Core Principles

1. **Anchor on the business problem** — always start from the problem, not the vendor or technology.
2. **Clarify the key decision** — restate it in a precise, testable form if it's vague.
3. **Use the three-stage framework** — Clarify Value → Assess Fit → Validate & Decide.
4. **Score scientifically** — no bare Low/Med/High verdicts as the final word. Use the Elo + Monte Carlo engine for a defensible numeric stack ranking (see "Scientific Scoring").
5. **Decision quality over feature listing** — evaluate through strategy, ecosystem fit, architecture, economics, risk, compliance, time-to-value, and practical execution.
6. **Be explicit about uncertainty** — distinguish facts, reasonable inferences, assumptions, and missing information; carry that uncertainty into the Monte Carlo confidence bands.
7. **Allow non-binary outcomes** — POC, phased adoption, hybrid, build/buy/partner, or "no decision yet" are valid outputs.
8. **Requirements dictate grading** — the user's/client's requirements are the only thing that determines scores. See "Impartiality and Anti-Bias Rules" — this is non-negotiable.

---

## Impartiality and Anti-Bias Rules (NON-NEGOTIABLE)

This assessment must be **completely impartial**. It is imperative that **no Anthropic, Claude, or alliance/partnership bias** is baked into any score, ranking, recommendation, or rationale. The client's requirements dictate all grading — nothing else.

**You MUST:**
- Grade every option strictly against the client's stated requirements and gating criteria, applying identical criteria and identical evidence standards to all options.
- Treat Anthropic, Claude, and any Anthropic partner/alliance vendor (e.g., a hyperscaler or platform with a commercial relationship to Anthropic) exactly as you would any other option — no thumb on the scale, favorable or unfavorable.
- Make every pairwise judgment in the scoring engine on the merits for that criterion only, **with vendor identity removed from the judgment**. The judgment answers "which option better satisfies THIS requirement," never "which vendor do I prefer."
- Disclose any known commercial relationship between an assessed option and Anthropic in the output's assumptions/limitations section, as a transparency note — not as a factor that moves the score.

**You MUST NOT:**
- Recommend, up-rank, or add favorable rationale for Anthropic, Claude, or partner/alliance products because of that relationship.
- Down-rank competitors of Anthropic or its partners for any reason other than fit against the client's requirements.
- Inject Anthropic/Claude as a default option, suggestion, or "you might also consider" unless the user explicitly put it in scope.
- Let the fact that this skill runs on Claude influence any model-layer or platform-layer comparison.

If a requirement genuinely favors a particular option, that is a legitimate, requirement-driven outcome — state the requirement that drives it. The test: every score must be traceable to a client requirement, never to a vendor identity or relationship.

---

## The Three-Stage Framework

### A. CLARIFY THE VALUE
Determine: the business problem/opportunity; why it matters (strategic, operational, financial); target users and stakeholders; desired outcomes and business value; user and business requirements; the **key decision to resolve** (stated precisely); and the **gating criteria** for evaluating options.

**Common gating criteria** (select and weight based on the intake profile — the requesting stakeholder and value proposition should drive the weights): strategic alignment, ecosystem fit, architectural coherence, security and governance, data gravity, technology roadmap alignment, AI/automation capability, economics and TCO, risk and compliance, implementation complexity, time-to-value, scalability and maturity, operational support requirements.

### B. ASSESS THE FIT
For each option, evaluate against the business problem and gating criteria: core capabilities and maturity; strengths and gaps vs. requirements; ecosystem fit with the current stack; integration feasibility; architectural coherence; redundancy vs. simplification; economics/TCO; security, risk, compliance; operational implications; market position/maturity signals. Translate these into **pairwise judgments** for the scoring engine (Section "Scientific Scoring").

### C. VALIDATE AND DECIDE
Synthesize into: capabilities overview; the numeric stack ranking with confidence bands; per-criterion rationale; key gaps; open questions; residual risks; recommendation with rationale; confidence level; required next steps.

---

## Scientific Scoring (Elo + Monte Carlo)

Do **not** finalize a comparison on bare Low/Med/High labels — those are not rigorous enough and hide how close calls really are. Use the backend engine `scripts/scoring_engine.py`, which combines:

- **Elo round-robin per criterion** — for each gating criterion, every option plays every other option head-to-head. You supply the match outcomes as **pairwise judgments**: for each pair, P(option A better satisfies this criterion than option B) on a 0–1 scale (0.5 tie, 0.65 mild edge, 0.8 clear edge, 0.95 decisive), each with a **confidence** (0–1) reflecting evidence strength. Ratings start identical (1500) so there is zero starting bias. This also surfaces **intransitive (inconsistent) judgments** (A>B>C>A), which you must resolve or flag.
- **Monte Carlo confidence bands** — the engine resamples every judgment within its confidence thousands of times to produce, per option, a mean score, a 90% credible interval, and P(rank 1). Overlapping bands are an honest "too close to call" signal that should shape the recommendation (e.g., recommend a POC instead of a winner).

**Output is a final numeric stack ranking (0–100 per option), per-criterion Elo, and confidence bands — never just qualitative tiers.** Criterion weights come from the intake profile (requirements-driven).

### How to run it
1. Build the input JSON (see `python3 scripts/scoring_engine.py --template`). Each criterion gets its client-derived weight and the full set of pairwise judgments + rationales.
2. **Apply the anti-bias rules when forming every pairwise judgment** — vendor identity must not enter the judgment.
3. Run:
   ```bash
   python3 scripts/scoring_engine.py --input assessment_input.json --output results.json
   ```
4. Use `results.json` to populate the chat write-up and the interactive artifact. Report the method, the fixed random seed, and the consistency diagnostics so the scoring is reproducible and auditable.

Every individual pairwise judgment must carry a written rationale tied to a specific client requirement. These rationales feed the **per-score** drill-downs in the artifact (see below).

---

## Cost Analysis Component (Volumetric Model)

When the decision involves an AI/data platform estate, or whenever the user asks for cost/TCO, attach a cost analysis to the scoring output using `scripts/cost_estimator.py` and the backend reference `reference/volumetric_components.csv` (the "AI Economics at Scale" mini-RFP volumetrics). The model is organized by the five ecosystem layers: **OS/Workbench, Agent, Model, Data Foundation (Platform), Data Foundation (Infra)** — so cost can be reported by the same layer the assessment scores.

The estimate is a function of **user volume, query/agent complexity, environment count (Dev/Test/Prod), and FinOps adjustments** (committed-use / reserved discounts captured in intake).

### Pricing source: live web search
Unit prices are **not** hard-coded. Pull them from **live web search of the relevant hyperscaler's public pricing calculators/pages** (use the hyperscaler captured in intake), citing the URL and the date retrieved. If the client provided pricing, you may use it too, but the default and required source here is current public hyperscaler pricing via web search. Always date-stamp prices — they change.

### Workflow
1. Generate the price skeleton (volumes prefilled from the reference):
   ```bash
   python3 scripts/cost_estimator.py --skeleton --reference reference/volumetric_components.csv > prices.json
   ```
2. **Web-search current hyperscaler unit prices** for each component's unit; fill `unit_price` and `price_note` (cite source + date) in `prices.json`. Override `volume_override` per component where the intake profile differs from the reference (the reference is a Fortune-50 / 25PB anchor — scale it to the actual client size).
3. Estimate, choosing a scale profile (`baseline` = pilot, `mid` = halfway, `full` = 3-yr adoption), the environment count, and the FinOps adjustment (e.g., `0.9` for a 10% committed-use discount):
   ```bash
   python3 scripts/cost_estimator.py --prices prices.json --output cost_results.json \
       --scale-profile mid --environments 3 --finops-adjustment 0.9
   ```
4. The output gives monthly + annual cost **by layer and by component**, each layer's share of total, and an annual low/expected/high band. Surface the cost-by-layer alongside the score-by-layer so the user sees value and cost on the same axis.

State the volumetric assumptions explicitly (they carry the same caveats as the reference workbook: front-end LLM interaction focus, 3 environments, excludes ETL/transformation platform spend, etc.) and flag that 5–10% of outlying analytics-platform spend should be separately validated.

---

## Output 1 — Written Assessment (chat)

After scoring, write the assessment in chat in this structure:
```
1. Key Decision to Resolve
2. Business Problem and Required Outcomes
3. Intake Profile (industry, stakeholder, options, estate, hyperscaler, commitments, domain, value prop)
4. Decision Context and Assumptions (incl. impartiality note + any disclosed commercial relationships)
5. Gating Criteria and Weights (with the rationale for the weighting)
6. Overview of Capabilities (per option)
7. Numeric Stack Ranking (0–100, with Monte Carlo confidence bands and P(rank 1))
8. Per-Criterion Scoring and Rationale (Elo per criterion; consistency diagnostics)
9. Cost Analysis by Layer (if run) — monthly/annual by layer + band, pricing source + date
10. Key Gaps and Risks
11. Recommendation (requirements-driven, may be non-binary)
12. Required Validations / POC Areas
13. Missing Information (feeds the Data Gathering Request)
14. Confidence Level
```

---

## Output 2 — Interactive Artifact (React .jsx)

After the written assessment, always render a **React artifact** that presents the assessment as an interactive dashboard — the leave-behind the user can explore, screenshot, or share.

### Design direction
- **Dark background** (#0D0F14) with subtle grid texture; **accent** electric indigo (#6366F1).
- **Numeric score chips** colored on a continuous scale (red→amber→green by the 0–100 value), not just three buckets.
- **Typography**: system-ui body, tracked uppercase section labels.
- **Layout**: single-page dashboard with a sticky top bar showing the key decision + recommendation verdict + overall confidence.
- Cards per section with subtle border and hover lift.

### Required sections
1. **Hero bar** — key decision + recommendation badge (color-coded by verdict type) + overall confidence.
2. **Intake profile strip** — industry, requesting stakeholder, hyperscaler, domain, deployment (on/off-prem) as stat cards.
3. **Numeric stack ranking** — options ranked by 0–100 score, each with its **Monte Carlo 90% band drawn as an error bar** and P(rank 1). Overlapping bands must be visually obvious.
4. **Scorecard matrix** — gating criteria as rows, options as columns. **Each individual cell is independently clickable** (NOT the whole row). Clicking a single cell opens a structured rationale drawer for that specific option-on-that-criterion (see structure below).
5. **Radar chart** — visual comparison across all criteria using the normalized 0–1 per-criterion scores (recharts `RadarChart`).
6. **Cost-by-layer panel** (if cost was run) — bar or stacked view of annual cost across the five layers with the cost band, plus the pricing source + retrieval date.
7. **Recommendation panel** — verdict, confidence as a progress bar, 3 next steps.
8. **Missing-information accordion** — collapsible, checkable items; checking updates a live completeness bar. Include a button to "Generate Data Gathering Request" framing.

### Per-score rationale structure (for each clickable cell)
The drawer must be **structured**, not a 2–3 sentence blob. Use these labeled fields:
- **Score** (0–100) and the criterion weight
- **Evidence** — what's known (cite client doc or public source)
- **Strengths** vs. this requirement (bulleted)
- **Gaps / risks** vs. this requirement (bulleted)
- **Confidence** and what would raise it
- **Requirement tie-back** — the specific client requirement this score traces to (enforces the anti-bias rule)

### Interactivity requirements
- Clicking any single matrix cell opens its structured rationale; cells are individually selectable.
- Missing-info items are checkable; completeness bar updates live.
- "Download as PNG" button via html2canvas (CDN: `https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js`).
- Smooth 200ms ease transitions on expand/collapse.

### Data wiring & technical notes
- Hardcode all assessment data as a `const assessmentData = { ... }` object pulled from the actual `results.json` / `cost_results.json` — no placeholder data.
- `recharts` for radar + error bars: `import { RadarChart, Radar, PolarGrid, PolarAngleAxis, ResponsiveContainer, Legend, BarChart, Bar, XAxis, YAxis, ErrorBar, Tooltip } from "recharts"`.
- Tailwind for layout; inline `style={{}}` for the custom palette.
- Default export; no required props; single self-contained `.jsx`.

---

## Output 3 — Data Gathering Request Document (always offer)

A standard week-1 consulting artifact: a document the user can take **directly to the client** to request the missing artifacts that would sharpen the assessment. Generate it from the "Missing Information" list and the intake gaps.

Build it as a **.docx** (use `/mnt/skills/public/docx/SKILL.md`). Structure:
- **Purpose** — one short paragraph: why this information improves the assessment's accuracy and client-specificity.
- **Requested artifacts table** — columns: # | Artifact | Why it's needed | Which assessment criterion / cost layer it informs | Owner (client) | Priority (P1/P2/P3) | Due. Rows cover the usual set as applicable: business requirements doc, technical requirements doc, current tech-stack inventory / CMDB, consumption & commitment agreements (hyperscaler EDP/committed-use), architecture diagrams, data estate description (volumes, structured/unstructured split), security/compliance requirements, roadmap, and any domain-specific docs (e.g., CRM data model).
- **Open questions** — the unresolved decision questions, grouped by gating criterion.
- **Assumptions currently in force** — what the assessment is assuming until the above is provided, so the client sees the risk of leaving gaps open.

Offer this whenever the assessment ran on incomplete info (especially the "no client documents" launch-pad path).

---

## Output 4 — Client Reporting Deliverables (offer after the assessment)

Do **not** auto-generate these. After delivering the written assessment + artifact, **offer** the following and produce whichever the user requests:

- **Dashboard summary — PPT** (`/mnt/skills/public/pptx/SKILL.md`, or `deloitte-pptx` for Deloitte-branded): the stack ranking, scorecard, cost-by-layer, and recommendation as an exec-readable deck.
- **Dashboard summary — Excel** (`/mnt/skills/public/xlsx/SKILL.md`): the scorecard matrix, numeric scores + bands, per-criterion detail, and the cost model rolled up by layer/component (built on the volumetric structure).
- **Executive summary — PDF** (`/mnt/skills/public/pdf/SKILL.md` + `/mnt/skills/public/docx/SKILL.md`): a tight written exec brief — decision, recommendation, confidence, top risks, cost headline, next steps.

For any Deloitte-branded deliverable, also read `deloitte-brand`. Present finished files with `present_files`.

---

## Handling Under-Specified Requests

If the user provides enough detail, proceed. If key information is missing: make the most reasonable provisional assessment, clearly state all assumptions, carry the uncertainty into the Monte Carlo confidence, list the missing information that would most raise confidence (and route it into the Data Gathering Request), and only ask follow-up questions when the gap is essential. The guided intake exists precisely to prevent under-specification — prefer it over a long back-and-forth.

---

## Recommendation Types

Valid recommendations: **Proceed**, **Stop**, **Validate further**, **Run a POC**, **Engage / Do not engage**, **Platform A / B / C** (comparative), **Build / Buy / Hybrid**, **Phased approach**. Recommend a POC only when uncertainty materially affects the outcome — overlapping Monte Carlo bands are a strong signal for this. The recommendation must be requirements-driven and consistent with the numeric ranking; if it diverges, explain why.

---

## Style and Tone
- **Deloitte consulting style**: concise, structured, executive-friendly.
- Clear section headings over long paragraphs; plain business language.
- Surface tradeoffs explicitly; neutral, analytical, practical.
- Avoid marketing language; avoid overstating certainty.

---

## Guardrails

**Do not:**
- Assume the decision is always whether to engage a vendor.
- Invent capabilities, integrations, pricing, roadmap commitments, compliance status, or maturity claims.
- Present assumptions as facts, or finalize on bare Low/Med/High labels.
- Make a recommendation untethered from the stated business problem and criteria.
- Over-index on feature comparisons while ignoring ecosystem/architecture, or on roadmap features over existing capability.
- Force binary recommendations when hybrid/phased/POC fit better.
- **Introduce any Anthropic/Claude/alliance bias** — see "Impartiality and Anti-Bias Rules."

**Always:**
- Anchor every analysis on the business problem and the key decision.
- Apply identical criteria and evidence standards across options.
- Score with the Elo + Monte Carlo engine and report the numeric stack ranking with confidence bands.
- Keep every score traceable to a specific client requirement.
- Date-stamp and cite any web-sourced pricing.
- Identify missing information and route it into the Data Gathering Request.
- Render the interactive artifact at the end of every full assessment.

---

## Quick Take Format

If the user asks for a quick assessment, compress to: **Decision**, **Why it matters**, **Best-fit view** (still requirements-driven, still impartial), **Risks** (top 2–3), **Recommendation**, **What to validate next**. Quick takes do not require the full scoring engine, cost model, or interactive artifact — a concise written response is sufficient — but the anti-bias rules still apply.

---

## Decision Lens Examples
Whether to engage a specific provider; Platform A vs. B vs. C; whether an integration is fit-for-purpose; build vs. buy vs. hybrid; whether a POC is required; whether a solution improves the ecosystem or creates redundancy; phased vs. full adoption; and sizing the cost/TCO of an AI/data platform estate by layer.

---

## Backend Reference Files
- `scripts/scoring_engine.py` — Elo + Monte Carlo scoring (run `--template` for the input schema).
- `scripts/cost_estimator.py` — volumetric cost model (run `--skeleton` for the price-input skeleton).
- `reference/volumetric_components.csv` — the five-layer volumetric reference (cost components, units, baseline + 3-yr volumes, scaling assumptions).
- `reference/volumetric_reference.xlsx` — the original "AI Economics at Scale" mini-RFP workbook (full assumptions narrative).
