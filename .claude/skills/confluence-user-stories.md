---
description: Scans an entire Confluence space, identifies features without corresponding Jira stories, and bulk-creates user stories for the coverage gaps. Cross-references existing Jira tickets to avoid duplicates. Use when inheriting a space with undocumented features or needing full Jira coverage for an initiative. Invoke with a Confluence space key and Jira project key.
dependencies:
  - Confluence: retrieve space page list, read individual pages
  - Jira: search existing stories, create issues, link epic, add labels
---

# /confluence-user-stories — Confluence Coverage Audit

## Invoke

```
/confluence-user-stories
Space: TEAM
Jira project: SQUAD1
Epic: SQUAD1-100   (optional — links all generated stories to this epic)
Filter: checkout   (optional — keyword to narrow which pages are processed)
```

## 1 — Scan the space

Retrieve all pages from the specified Confluence space — if a `Filter` keyword was provided, limit to pages whose title or content contains that keyword — record title, page ID, last updated date, and any existing Jira links in the content.

## 2 — Read each page

For each in-scope page, extract features described, requirements stated, user flows, and personas mentioned.

Skip pages that are: meeting notes, sprint pages, retrospectives, runbooks, onboarding guides, or index/navigation pages.

## 3 — Cross-reference Jira

For each extracted feature, search Jira for existing stories using the feature name and key terms:

| Match | Action |
|-------|--------|
| Open or in-progress story found | Mark as **Covered** — do not create |
| No story found | Mark as **Gap** — queue for creation |

## 4 — Generate stories for gaps

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

## 5 — Bulk create in Jira

Create all Gap stories with label `pm-agent-generated`, epic link if provided, and Confluence source page URL in description.

Batch limit: if more than 20 stories are to be created, confirm before proceeding.

## 6 — Report

Output a summary table:

| Story Key | Summary | Source Page | Template |
|-----------|---------|-------------|----------|
| SQUAD1-301 | As a user… | Product Features | Standard |

Include: total pages scanned, total features extracted, stories created (with keys), features skipped (already covered in Jira), and pages skipped (ceremony/ops).

## Output

Jira issues created for every undocumented feature gap found in the specified Confluence space.

**Side effects:** Creates Jira issues with label `pm-agent-generated`. Each issue includes the source Confluence page URL. If an epic key was provided, all stories are linked to it.

## Guidelines

- Never create a story for something already tracked in Jira — always check first.
- If a page has no extractable features, skip it and note it in the report.
- If a feature is ambiguous, create the story with an explicit assumption in Technical Notes rather than skipping it.
- If the space has 500+ pages, ask whether to process all at once or a subset filtered by keyword or date range.
