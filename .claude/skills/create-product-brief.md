---
description: "Drafts a product brief from an idea — problem statement, target user, success metrics, scope. Run before /create-prd. Seeds the PRD."
version: "1.1.0"
last_updated: "2026-04-02"
bmm_phase: "01_Accelerated_Context_Discovery"
bmm_step: "product_brief"
bmm_agent: pm
bmm_runs: standalone_or_orchestrated
output_file: "tools/bmm/output/briefs/product-brief.md"
output_contract:
  required_sections:
    - Problem Statement
    - Target User
    - Success Metrics
    - Scope
    - Out of Scope
  required_fields:
    problem_statement: [what, who, why_now, current_workaround]
    target_user: [segment, context, job_to_be_done, pain_intensity]
    success_metrics: [primary_kpi, secondary_kpis, time_to_validate]
skip_if_exists: true
handoff_writes:
  - key: brief_complete
    value: true
  - key: brief_output
    value: "tools/bmm/output/briefs/product-brief.md"
dependencies:
  confluence:
    actions: [search, read]
    required: false
---

# /create-product-brief — Product Brief

## Invoke

```
/create-product-brief
Initiative: [short name — e.g. "One-tap Checkout"]
Idea: [1–3 sentence description of the problem or opportunity]
```

Or invoke with a pre-filled strategic core (skips discovery questions):

```
/create-product-brief
Initiative: [short name]
What: [specific friction or gap — one sentence]
Who: [user segment experiencing it]
Why now: [market timing or urgency signal]
Workaround: [what users do today instead]
Segment: [e.g. loyalty member, new shopper]
Context: [where/when they encounter the problem]
JTBD: [underlying goal — not the feature request]
Pain: [low | medium | high | critical]
Primary KPI: [north-star metric with baseline → target]
Secondary KPIs: [2–3 supporting metrics]
Validate in: [e.g. "6 weeks post-launch"]
```

## 1 — Load existing context

Search Confluence for related PRDs, research reports, and prior briefs using the initiative name and key terms. Read the 3–5 most relevant pages to:
- Confirm the problem hasn't been solved by a shipped feature
- Surface any existing data or research that supports the brief
- Identify terminology the team already uses for this space

Check `tools/bmm/output/research/research-findings.md` if it exists — pre-populate the brief's opportunity data from Bumblebee's research.

## 2 — Discover missing fields

For any `required_fields` left blank in the invocation, run targeted discovery:

| Missing field | Discovery question |
|---|---|
| `what` | "What specific friction or gap does this address — one sentence?" |
| `who` | "Which user segment experiences this most acutely?" |
| `why_now` | "What's changed in the market or product that makes this urgent now?" |
| `current_workaround` | "What do users do today when they hit this friction?" |
| `job_to_be_done` | "What underlying goal is the user trying to achieve — not the feature?" |
| `pain_intensity` | "Is this friction low / medium / high / critical for that user?" |
| `primary_kpi` | "What's the single north-star metric — what's the current baseline and target?" |
| `time_to_validate` | "How long after launch do we need to see signal?" |

Ask all missing questions in one block — do not drip-feed one at a time.

## 3 — Draft the brief

Write to `tools/bmm/output/briefs/product-brief.md` using this structure:

```markdown
---
title: "[Initiative] — Product Brief"
date: [YYYY-MM-DD]
status: draft
bmm_phase: 01
stepsCompleted: []
inputDocuments: []
---

# [Initiative] — Product Brief

## Problem Statement
**What:** [specific friction or gap]
**Who:** [user segment]
**Why now:** [urgency signal]
**Current workaround:** [what users do today]

## Target User
**Segment:** [segment name]
**Context:** [where/when they encounter the problem]
**Job to be done:** [underlying goal]
**Pain intensity:** [low | medium | high | critical]

## Success Metrics
**Primary KPI:** [metric — baseline → target]
**Secondary KPIs:**
- [metric 1]
- [metric 2]
**CR impact hypothesis:** [directional e.g. "+2–4% checkout CR"]
**AOV impact hypothesis:** [directional or N/A]
**Validate in:** [timeframe]

## Scope (In)
- [capability or outcome — not feature names]

## Out of Scope
- [explicit exclusions]

## Open Questions
- [anything unresolved at brief stage]
```

## 4 — Review with user

Present the complete brief. Ask:
- "Does this accurately capture the problem and opportunity?"
- "Any scope items to add or remove before we move to research and PRD?"

Iterate on feedback before marking complete.

## Output

`tools/bmm/output/briefs/product-brief.md` — fully populated product brief ready to seed the PRD.

**In orchestrated mode:** Optimus Prime writes the brief concurrently while Bumblebee runs `/market-research`. Both outputs feed the Strategic Alignment gate.

## Failure Modes

| Condition | Behaviour |
|---|---|
| Brief already exists at output path | Load and present existing brief — confirm with user before overwriting (`skip_if_exists: true`) |
| Initiative name not provided | Ask for it before any other discovery — do not proceed without a name |
| `pain_intensity: critical` claimed without data | Reject it — ask for supporting data or a quoted user insight before accepting |
| Confluence search returns no relevant results | Proceed without prior context — note "No prior Confluence context found" in Open Questions |
| Research findings file exists but is empty or malformed | Skip it and note the gap in Open Questions — do not fail |

## Guidelines

- The brief is not a PRD — no functional requirements, no solution details, no acceptance criteria.
- `pain_intensity: critical` requires supporting data or a quoted user insight. Do not accept it without evidence.
- Every success metric must be measurable within `time_to_validate`. Vague metrics ("improve satisfaction") are rejected.
- If `skip_if_exists: true` and `tools/bmm/output/briefs/product-brief.md` already exists, load it and confirm with the user before overwriting.
- Calibrate explanation depth to `{user_skill_level}` from config:
  - `beginner` — walk through each field with an example before asking for input
  - `intermediate` — standard discovery flow, confirm ambiguous fields
  - `expert` — skip preamble, present the draft structure and ask for gaps only
