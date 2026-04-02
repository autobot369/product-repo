---
description: "Converts story intent into full Gherkin stories and pushes to Jira. Auto-selects template per story. Optionally assigns to next sprint."
version: "1.1.0"
last_updated: "2026-04-02"
bmm_phase: "04_One_Shot_Backlog"
bmm_step: "gherkin_stories"
bmm_agent: sm
bmm_runs: standalone_or_orchestrated
bmm_reads:
  - "tools/bmm/output/prds/final-prd.md"
  - "tools/bmm/output/stories/story-intent.md"
output_file: "tools/bmm/output/stories/"
output_contract:
  format: gherkin
  required_per_story:
    - Given/When/Then blocks
    - acceptance_criteria
    - prd_requirement_reference
  post_process: gherkin_validator
handoff_writes:
  - key: stories_complete
    value: true
  - key: stories_output
    value: "tools/bmm/output/stories/"
dependencies:
  confluence:
    actions: [search, read]
    required: false
  jira:
    actions: [search, create, get_sprints, assign_sprint]
    required: true
---

# /user-stories — User Story Generator

## Invoke

```
/user-stories
PRD: https://your-org.atlassian.net/wiki/spaces/TEAM/pages/[page-id]  (optional)
Jira project: SQUAD1
Epic: SQUAD1-42  (optional)
Board ID: 7      (optional — assigns stories to next upcoming sprint)
```

## 1 — Load requirements source

| Signal | Action |
|--------|--------|
| `story-intent.md` exists at `tools/bmm/output/stories/story-intent.md` | Read it as primary input — use intent entries as the story scaffold |
| PRD URL provided | Fetch the Confluence page — extract goal, success metrics, personas, features, acceptance conditions, constraints, out-of-scope items, and open questions |
| Neither available | Search the Confluence space using the epic name or project context — read 5–8 most relevant pages — list source pages in the final report |

## 2 — Resolve sprint

Call `get_jira_sprints(board_id)` — pick the earliest sprint with `state = "future"`; fall back to `state = "active"` if none exists — store the sprint ID for Step 7.

Skip this step if no Board ID was provided.

## 3 — Gather additional Confluence context

Search for related pages (architecture docs, API specs, prior retrospectives) — read 3–5 most relevant to surface technical constraints, avoid duplicating shipped functionality, and source correct team terminology.

## 4 — Check for existing Jira coverage

Search Jira for existing stories related to each extracted feature — skip any feature already tracked in an open or in-progress story — note skipped items in the final report.

## 5 — Generate stories

Derive stories across 5 dimensions:
1. Happy path (primary user flow)
2. Fallback / empty states
3. Data freshness and loading states
4. User control and feedback (errors, confirmations, undo)
5. Edge cases surfaced by Open Questions

Auto-select template per story:

| Story title signals | Template |
|--------------------|----------|
| API, endpoint, integration, sync, migration, webhook, schema, database, queue, event, performance, auth, token, permissions | **Technical** |
| scenario, flow, journey, checkout, onboarding, wizard, multi-step, conditional, eligibility, trigger | **Gherkin** |
| Everything else | **Standard** |

Every story includes:
- User Story Statement: `As a [persona], I want [action], so that [benefit]`
- Description: why this story exists and how it contributes to the epic goal
- Acceptance Criteria: 3–6 numbered, verifiable, testable conditions
- Technical Notes: endpoints, DB changes, auth constraints, dependencies (expanded for Technical template)
- Definition of Done: unit tests passing, PR approved, AC verified by QA/PM, documentation updated, no new high-severity warnings

**Bob's sizing rule:** if a story's scope implies more than 3 days of dev effort, split it before creating the Jira issue.

## 6 — Create Jira issues

Create each story with label `pm-agent-generated`, epic link if provided, and Confluence PRD URL in description if PRD was provided.

Batch limit: if more than 15 features are found, confirm before proceeding.

## 7 — Assign to sprint

Bulk-assign all created issue keys to the sprint resolved in Step 2 — print: `Assigned N stories to [Sprint Name]`.

Skip this step if no Board ID was provided.

## 8 — Run Gherkin validation

After all stories are created, run the Gherkin validator post-process:
- Verify every Gherkin story has at least one `Given`, one `When`, one `Then` block
- Verify every story has a PRD requirement reference
- Verify acceptance criteria are numbered and testable
- Report any failures — Bob re-runs failing stories only, not the full batch

## 9 — Report

Output a summary table:

| Key | Summary | Template | Sprint |
|-----|---------|----------|--------|
| SQUAD1-201 | As a user, I want… | Gherkin | Sprint 14 |

Include: total stories created, stories skipped (already in Jira), validation pass/fail count, and source pages used if no PRD was provided.

## Output

Jira issues created in the specified project, linked to the epic, and optionally sprint-assigned.

**Side effects:** Creates Jira issues with label `pm-agent-generated`. Sprint assignment is a bulk operation on the resolved sprint — not the active one unless no future sprint exists.

## Failure Modes

| Condition | Behaviour |
|---|---|
| No `story-intent.md` and no PRD URL provided | Search Confluence using epic/project context — note sources used in report |
| Jira unavailable | Write stories to `tools/bmm/output/stories/` as markdown files — note that Jira push failed; stories can be pushed manually |
| Board ID provided but no future sprint found | Fall back to active sprint — confirm with user before assigning |
| More than 15 features extracted | Pause and confirm before bulk-creating — present feature list first |
| Gherkin validator fails on one or more stories | Re-run failing stories only — do not regenerate the full batch |
| Story scope > 3 days dev effort | Split into sub-stories before creating the Jira issue — never create an oversized story |

## Guidelines

- Never duplicate a story that already exists in Jira — always check first.
- Unclear requirements are noted as assumptions in Technical Notes — never silently guessed.
- Sprint assignment uses only the resolved sprint from the board — never infer sprint names from context.
- If inputs are ambiguous, ask one clarifying question before generating.
- Gherkin scenario steps describe observable behaviour — not code calls or implementation detail.
- Calibrate explanation depth to `{user_skill_level}` from config:
  - `beginner` — explain Given/When/Then format with an example before writing; walk through AC criteria interactively
  - `intermediate` — standard execution; flag ambiguous requirements before writing AC
  - `expert` — generate all stories in one pass, run validation, present summary for approval
