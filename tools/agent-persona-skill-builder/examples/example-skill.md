---
description: Generates Jira user stories from a PRD URL or Confluence space search. Auto-selects Standard, Technical, or Gherkin template per story. Optionally sprint-assigns. Invoke with Jira project key; PRD and epic are optional.
---

# /user-stories — User Story Generator

## Invoke

```
/user-stories
PRD: https://your-org.atlassian.net/wiki/spaces/TEAM/pages/[id]  (optional)
Jira project: SQUAD1
Epic: SQUAD1-42   (optional)
Board ID: 7       (optional — assigns to next upcoming sprint)
```

## 1 — Load requirements source

| Input | Action |
|-------|--------|
| PRD URL provided | Fetch page — extract goal, personas, ACs, out-of-scope items, open questions |
| No PRD | Search Confluence with epic/project key — read 5–8 pages — list sources in report |

## 2 — Resolve sprint (if Board ID provided)

Call `get_jira_sprints(board_id)` — pick earliest `state: future`, fallback to `state: active`. Store sprint ID; do not assign yet.

## 3 — Check existing Jira coverage

Search Jira for stories matching each extracted feature. Mark as **Covered** (skip) or **Gap** (create). List skipped items in final report.

## 4 — Generate stories across 5 dimensions

For each Gap feature: happy path, fallback/empty states, loading states, user feedback (errors/undo), edge cases from open questions.

Auto-select template:

| Title signal keywords | Template |
|-----------------------|----------|
| API, endpoint, integration, webhook, schema, auth, migration, performance | Technical |
| flow, journey, checkout, wizard, multi-step, eligibility, trigger | Gherkin |
| Everything else | Standard |

Every story includes: user story statement, 3–6 ACs, technical notes, Definition of Done.

## 5 — Create Jira issues + assign sprint

Create each story with label `pm-agent-generated`, epic link (if provided), PRD URL in description. If > 15 stories, confirm before proceeding. Bulk-assign all to resolved sprint.

## Output

Summary table of created stories (key, summary, template, sprint). Includes stories skipped and source pages used.

**Side effects:** Creates Jira Story issues. Assigns to sprint if Board ID provided.

## Guidelines

- Never create a story that already exists in Jira — always check first.
- Note unclear requirements as explicit assumptions in Technical Notes — never guess silently.
- Sprint assignment uses only the board-resolved sprint — never infer from context.
- Ask one clarifying question if inputs are ambiguous before generating.
