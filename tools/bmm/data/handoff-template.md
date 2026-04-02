---
# BMM Phase Handoff Context
# Written by the completing agent at the end of each phase.
# Read by the next agent as its FIRST action before any work begins.
# Path: tools/bmm/output/handoff-[phase-number].md
#
# MANDATORY: Next agent must read this file completely before proceeding.
# MANDATORY: Do not delete — used by the orchestrator to verify gate passage.

handoff_version: "1.0"
written_by: ""           # agent name (e.g. pm, analyst, ux-designer, architect, sm)
written_at: ""           # ISO timestamp
phase_completed: ""      # e.g. 01_Accelerated_Context_Discovery
phase_next: ""           # e.g. 02_Solutioning_Sprint
gate_outcome: ""         # go | no-go | amend — outcome of the gate that closed this phase
gate_participants: []    # agents who participated in the gate
---

# Phase Handoff: [Phase Label]

## What was completed

[2–4 sentence summary of what the completing agent(s) produced and any significant
decisions or pivots made during the phase. Written in first person by the completing agent.]

## Outputs produced

| File | Agent | Status | Notes |
|------|-------|--------|-------|
| [path/to/file.md] | [agent] | complete | [any caveats] |

## Gate outcome: [go | no-go | amend]

**Participants:** [agent names]
**Decision:** [go | no-go | amend]
**Rationale:** [1–2 sentences — why this outcome was reached]

### Amendments required (if outcome = amend)
- [Specific change required — which file, which section, what must change]

### Blocking risks (if outcome = no-go)
- [What must be resolved before this workflow can proceed]

## Context for next agent

> Read this before starting [next phase label].

**Key decisions that affect your work:**
- [Decision 1 — why it matters for the next phase]
- [Decision 2]

**Assumptions to carry forward:**
- [Assumption 1 — source: brief / research / gate discussion]
- [Assumption 2]

**Open questions not yet resolved:**
- [Question 1 — owner: [agent]]
- [Question 2 — owner: [agent]]

**Do not re-open:**
- [Item 1 — this was debated in the gate and closed]
- [Item 2]

## Input documents loaded this phase

```yaml
inputDocuments:
  - type: local
    path: ""
    summary: ""
  - type: confluence
    title: ""
    url: ""
    page_id: ""
  - type: jira
    key: ""
    summary: ""
    status: ""
```

## Signals for the orchestrator

```yaml
orchestrator_signals:
  brief_complete: false
  research_complete: false
  prd_complete: false
  ux_journeys_complete: false
  architecture_complete: false
  story_intent_complete: false
  stories_complete: false
  gate_01_passed: false
  gate_02_passed: false
  gate_03_passed: false
  gherkin_validator_passed: false
```
