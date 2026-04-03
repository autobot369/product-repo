---
description: "Phase 04 story intent: extracts user stories from PRD and architecture for Ironhide's Gherkin run. Standalone: scans a Confluence space for undocumented feature gaps."
version: "1.1.0"
last_updated: "2026-04-02"
bmm_phase: "04_One_Shot_Backlog"
bmm_step: "story_intent"
bmm_agent: pm
bmm_runs: standalone_or_orchestrated
bmm_reads:
  - "tools/bmm/output/prds/final-prd.md"
  - "tools/bmm/output/architecture-decisions.md"
output_file: "tools/bmm/output/stories/story-intent.md"
output_contract:
  required_per_feature:
    - user_story_statement
    - acceptance_criteria
    - prd_section_reference
handoff_to: user-stories
handoff_writes:
  - key: story_intent_complete
    value: true
  - key: story_intent_output
    value: "tools/bmm/output/stories/story-intent.md"
dependencies:
  confluence:
    actions: [search, read]
    required: false
  jira:
    actions: [search, create, link_epic]
    required: true
---

# /confluence-user-stories — Story Intent

## Modes

This skill operates in two distinct modes:

**Orchestrated (Phase 04):** Optimus Prime reads `final-prd.md` and `architecture-decisions.md` to produce structured story intent — a user story statement, acceptance criteria, and PRD trace for each feature. Output is `story-intent.md`, which Ironhide's `/user-stories` run consumes directly.

**Standalone (coverage audit):** Given a Confluence space key and Jira project, scans the space for features without corresponding Jira stories and bulk-creates stories for the gaps. Use when inheriting a space with undocumented features.

---

## Invoke

**Orchestrated / intent mode:**
```
/confluence-user-stories
Jira project: SQUAD1
Epic: SQUAD1-100   (optional — links all stories to this epic)
```

**Standalone / audit mode:**
```
/confluence-user-stories
Space: TEAM
Jira project: SQUAD1
Epic: SQUAD1-100   (optional)
Filter: checkout   (optional — keyword to narrow which pages are processed)
```

---

## Orchestrated mode (Phase 04 — story intent)

### 1 — Load pipeline outputs

Read `tools/bmm/output/prds/final-prd.md` and `tools/bmm/output/architecture-decisions.md` completely. Extract:
- All functional requirements (each becomes at least one story)
- User journey steps that imply distinct user actions
- Non-functional requirements that need engineering stories
- Open Questions that must be resolved before implementation

### 2 — Produce story intent

For each extracted feature, write a story intent entry:

```markdown
### [Feature Name]
**User story:** As a [persona], I want [action], so that [benefit]
**Acceptance criteria:**
1. [testable condition]
2. [testable condition]
3. [testable condition]
**PRD reference:** §[section] — [requirement label]
**Architecture reference:** [entity or endpoint if applicable]
**Template hint:** [Standard | Technical | Gherkin] — why
**Notes:** [any open question or dependency to resolve before Ironhide runs Gherkin]
```

### 3 — Write output

Save to `tools/bmm/output/stories/story-intent.md`. Signal `story_intent_complete: true` in the handoff file.

---

## Standalone mode (Confluence coverage audit)

### 1 — Scan the space

Retrieve all pages from the specified Confluence space — if a `Filter` keyword was provided, limit to pages whose title or content contains that keyword — record title, page ID, last updated date, and any existing Jira links in the content.

### 2 — Read each page

For each in-scope page, extract features described, requirements stated, user flows, and personas mentioned.

Skip pages that are: meeting notes, sprint pages, retrospectives, runbooks, onboarding guides, or index/navigation pages.

### 3 — Cross-reference Jira

For each extracted feature, search Jira for existing stories using the feature name and key terms:

| Match | Action |
|-------|--------|
| Open or in-progress story found | Mark as **Covered** — do not create |
| No story found | Mark as **Gap** — queue for creation |

### 4 — Generate stories for gaps

For each Gap feature, write a user story using auto-template logic:

| Story title signals | Template |
|--------------------|----------|
| API, endpoint, integration, schema, auth, migration, performance | **Technical** |
| flow, journey, checkout, wizard, multi-step, conditional, trigger | **Gherkin** |
| Everything else | **Standard** |

Every story includes:
- User Story Statement: `As a [persona], I want [action], so that [benefit]`
- Acceptance Criteria: 3–5 numbered, verifiable conditions
- Technical Notes: constraints and dependencies surfaced from the Confluence page
- Source reference: Confluence page URL in the description
- Definition of Done: unit tests passing, PR approved, AC verified by QA/PM, documentation updated

### 5 — Bulk create in Jira

Create all Gap stories with label `pm-agent-generated`, epic link if provided, and Confluence source page URL in description.

Batch limit: if more than 20 stories are to be created, confirm before proceeding.

### 6 — Report

Output a summary table:

| Story Key | Summary | Source Page | Template |
|-----------|---------|-------------|----------|
| SQUAD1-301 | As a user… | Product Features | Standard |

Include: total pages scanned, total features extracted, stories created (with keys), features skipped (already covered in Jira), and pages skipped (ceremony/ops).

---

## Output

**Orchestrated:** `tools/bmm/output/stories/story-intent.md` — structured intent consumed by Ironhide's `/user-stories` run.

**Standalone:** Jira issues created for every undocumented feature gap found in the specified Confluence space.

**Side effects (standalone):** Creates Jira issues with label `pm-agent-generated`. Each issue includes the source Confluence page URL. If an epic key was provided, all stories are linked to it.

## Failure Modes

| Condition | Behaviour |
|---|---|
| `final-prd.md` not found (orchestrated mode) | Stop — ask user to complete the PRD phase before running story intent |
| `architecture-decisions.md` not found (orchestrated mode) | Proceed without architecture context — note missing tech references as gaps in story intent |
| No functional requirements extractable from PRD | Ask user to confirm the PRD is complete — do not generate placeholder stories |
| Space has 500+ pages (standalone mode) | Ask whether to process all at once or a filtered subset by keyword or date range |
| Jira unavailable | Write intent to `story-intent.md` only — note that Jira push failed; stories can be pushed manually later |

## Guidelines

- Never create a story for something already tracked in Jira — always check first.
- If a page has no extractable features (standalone), skip it and note it in the report.
- If a feature is ambiguous, create the story with an explicit assumption in Technical Notes rather than skipping it.
- If the space has 500+ pages, ask whether to process all at once or a subset filtered by keyword or date range.
- Calibrate explanation depth to `{user_skill_level}` from config:
  - `beginner` — walk through the story intent format with an example; confirm AC quality interactively
  - `intermediate` — standard execution; flag ambiguous features and ask for clarification before writing AC
  - `expert` — produce full story intent in one pass; surface assumptions for a single review
