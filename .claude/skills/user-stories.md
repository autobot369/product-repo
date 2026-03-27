---
description: Generates well-structured Jira user stories from a PRD URL or Confluence context search. Auto-selects story template (Standard / Technical / Gherkin) per story. Optionally assigns stories to the next upcoming sprint. Invoke with Jira project key; PRD URL and epic key are optional.
dependencies:
  - Confluence: search space, read pages
  - Jira: search existing stories, create issues, get sprints, assign to sprint
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
| PRD URL provided | Fetch the Confluence page — extract goal, success metrics, personas, features, acceptance conditions, constraints, out-of-scope items, and open questions |
| No PRD | Search the Confluence space using the epic name or project context — read 5–8 most relevant pages — list source pages in the final report |

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

## 6 — Create Jira issues

Create each story with label `pm-agent-generated`, epic link if provided, and Confluence PRD URL in description if PRD was provided.

Batch limit: if more than 15 features are found, confirm before proceeding.

## 7 — Assign to sprint

Bulk-assign all created issue keys to the sprint resolved in Step 2 — print: `Assigned N stories to [Sprint Name]`.

Skip this step if no Board ID was provided.

## 8 — Report

Output a summary table:

| Key | Summary | Template | Sprint |
|-----|---------|----------|--------|
| SQUAD1-201 | As a user, I want… | Gherkin | Sprint 14 |

Include: total stories created, stories skipped (already in Jira), and source pages used if no PRD was provided.

## Output

Jira issues created in the specified project, linked to the epic, and optionally sprint-assigned.

**Side effects:** Creates Jira issues with label `pm-agent-generated`. Sprint assignment is a bulk operation on the resolved sprint — not the active one unless no future sprint exists.

## Guidelines

- Never duplicate a story that already exists in Jira — always check first.
- Unclear requirements are noted as assumptions in Technical Notes — never silently guessed.
- Sprint assignment uses only the resolved sprint from the board — never infer sprint names from context.
- If inputs are ambiguous, ask one clarifying question before generating.
