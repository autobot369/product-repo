---
description: "Creates a fully structured PRD from a brief. Reads Confluence for context, avoids duplicates, and publishes under the configured parent page."
version: "1.1.0"
last_updated: "2026-04-02"
bmm_phase: "02_Solutioning_Sprint"
bmm_step: "prd_authoring"
bmm_agent: pm
bmm_runs: standalone_or_orchestrated
bmm_reads:
  - "tools/bmm/output/briefs/product-brief.md"
  - "tools/bmm/output/research/research-findings.md"
output_file: "tools/bmm/output/prds/final-prd.md"
output_contract:
  required_sections:
    - Problem & Opportunity
    - Objective
    - Success Metrics
    - Functional Requirements
    - Non-Functional Requirements
    - User Journeys
    - Out of Scope
  min_success_metrics: 2
handoff_writes:
  - key: prd_complete
    value: true
  - key: prd_output
    value: "tools/bmm/output/prds/final-prd.md"
dependencies:
  confluence:
    actions: [search, read, create, update]
    required: true
  jira:
    actions: [read_epic]
    required: false
---

# /create-prd — PRD Creator

## Invoke

```
/create-prd
Initiative: [short name]
Business Problem: [metric or outcome at risk — include data if available]
User Problem: [friction or unmet need from the user's perspective]
Ideal Solution: [what to build — feature names or a paragraph]
Metrics: [KPIs — targets optional]
```

## 1 — Gather Confluence context

Search the Confluence space using the initiative name and key feature terms — read the 3–5 most relevant pages to validate the problem, avoid duplicating shipped features, and source correct team terminology.

| Query | Purpose |
|-------|---------|
| `[Initiative name]` | Existing PRDs and epics |
| `[key feature terms] PRD` | Related shipped features |
| `[user persona] requirements` | Prior requirements docs |

## 2 — Generate PRD content

Build the full PRD using this structure:

| Section | Contents |
|---------|----------|
| Header table | Target release, Epic, Status (Draft), Owner, PMs, Designer, Tech Lead, QA |
| 🤔 Problem & Opportunity | Journey flow (Path A current / Path B ideal), context data, The Gap, The Value |
| 🎯 Objective | One-paragraph goal statement tied to the business metric |
| 📊 Success Metrics | 2–4 metrics: Goal, KPI, type (leading/lagging), definition, tracking event name |
| 📋 Requirements | 4–8 user stories: requirement, acceptance criteria, importance (Must/Should/Could) |
| 🎨 Design | Figma placeholder — note "Link to be added after UX kickoff" |
| ❓ Open Questions | 4–6 pre-grooming questions with partial answers where known |
| ⭐ Timeline | Sprint phase table: UX Prep → Grooming → Dev → QA → Go-live |

| Input signal | Behaviour |
|---|---|
| Inputs are sparse | Make reasonable inferences — flag each in Open Questions |
| Matching page already exists | Update it rather than creating a duplicate |
| Metric or claim can't be sourced from context | Mark as placeholder — never invent data |

Leave a `<!-- Sally: embed journeys here -->` placeholder in the Functional Requirements section — do not author UX journeys yourself.

## 3 — Create or update Confluence page

Check for an existing page under the configured PRD parent (`tools/config.yml` → `pm_workers.prd_parent_page_id`):

| State | Action |
|-------|--------|
| Page exists | Update the existing page |
| No page exists | Create a new child page under the PRD parent |

Add labels: `prd`, `draft`

## 4 — Report

Output the Confluence page URL followed by a next-steps checklist:
- [ ] Add Figma link once UX kickoff is complete
- [ ] Fill in target release and team assignments
- [ ] Answer Open Questions before grooming session
- [ ] Run `/ux-journeys` to embed user journeys into Functional Requirements
- [ ] Run `/user-stories` with the PRD URL to generate Jira stories

## Output

Confluence page containing the fully structured PRD, published under the configured parent page.

**Side effects:** Creates or updates a Confluence child page with labels `prd`, `draft`.

## Failure Modes

| Condition | Behaviour |
|---|---|
| `product-brief.md` not found | Ask user to run `/create-product-brief` first — proceeding without a brief produces a lower-quality PRD; confirm intent before continuing |
| `research-findings.md` not found | Proceed without research context — note "No prior research loaded" in Open Questions |
| All required inputs missing (no Initiative, no Business Problem) | Ask for Initiative name and Business Problem before generating — minimum viable inputs |
| Existing PRD page found in Confluence | Update it rather than creating a duplicate — confirm with user if substantial changes are implied |
| `min_success_metrics` cannot be met from inputs | Ask for missing metrics explicitly — do not invent them or use vague placeholders |
| Confluence unavailable | Write PRD to `output_file` only — note that Confluence publish failed in the report |

## Guidelines

- Never hallucinate product data — if a metric can't be sourced from Confluence context, mark it as a placeholder.
- Do not generate stories in this skill — that is the job of `/user-stories`.
- Do not author UX journeys — leave the placeholder for Sally's `/ux-journeys` run.
- If the initiative already has an active Jira epic, note it in the header table.
- Keep requirement statements in user story format: *As a [persona], I want [action], so that [benefit].*
- Calibrate explanation depth to `{user_skill_level}` from config:
  - `beginner` — explain each PRD section before writing it; offer to walk through inputs interactively
  - `intermediate` — standard execution; confirm ambiguous inputs before proceeding
  - `expert` — generate the full draft, flag assumptions, ask for a single pass review
