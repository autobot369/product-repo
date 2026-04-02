---
description: Defines the data model and API contracts for a feature based on a locked PRD. Scoped to data-model-and-APIs only — no infrastructure decisions. Run sequentially after the PRD and UX journeys are locked (Phase 03). Feeds the Implementation Readiness gate.
bmm_phase: "03_Architecture_and_Readiness"
bmm_step: "arch_alignment"
bmm_agent: architect
bmm_runs: standalone_or_orchestrated
bmm_reads:
  - "tools/bmm/output/prds/final-prd.md"
  - "tools/bmm/output/research/research-findings.md"
  - "docs/specs/"
output_file: "tools/bmm/output/architecture-decisions.md"
output_contract:
  required_sections:
    - Context Summary
    - Data Model
    - API Contracts
    - Key Decisions
    - Open Technical Risks
  required_per_api:
    - endpoint
    - method
    - request_schema
    - response_schema
    - auth_requirements
    - error_codes
  min_decisions: 3
handoff_writes:
  - key: architecture_complete
    value: true
  - key: architecture_output
    value: "tools/bmm/output/architecture-decisions.md"
dependencies:
  - Confluence: read existing specs, API docs, architecture decision records
  - Jira: read related technical epics (optional)
---

# /create-architecture — Architecture Alignment

## Invoke

```
/create-architecture
PRD: tools/bmm/output/prds/final-prd.md
Scope: data-model-and-apis     (default — do not expand to infrastructure)
```

Or in orchestrated mode — Winston activates automatically after Technical Readiness gate approval.

## 1 — Load and parse the PRD

Read `tools/bmm/output/prds/final-prd.md` completely. Extract:

- All functional requirements — each one implies at least one data entity or API call
- All user journey steps — each step that involves data persistence or retrieval needs a model and an endpoint
- Non-functional requirements — latency, throughput, and consistency constraints
- Success metrics — understand the data events that must be tracked
- Out of scope — hard boundaries on what Winston must not design for

Also read:
- `docs/specs/` — existing technical specifications to avoid conflicting data models
- Confluence architecture decision records if available — maintain consistency with prior decisions

## 2 — Define the data model

For each entity implied by the PRD's functional requirements:

```markdown
### Entity: [EntityName]

| Field | Type | Constraints | Notes |
|-------|------|-------------|-------|
| id | UUID | required, unique | |
| [field] | [type] | [constraints] | [why this field exists — link to PRD requirement] |

**Relationships:**
- [EntityName] has-many [OtherEntity] via [foreign_key]
- [EntityName] belongs-to [OtherEntity]

**Indexes required:**
- [field] — reason: [query pattern this serves]

**PRD traceability:** Functional Requirement §[X.Y]
```

Every entity must trace back to at least one PRD functional requirement. Entities with no PRD trace are out of scope.

## 3 — Define API contracts

For each user action in the journey that requires a network call:

```markdown
### [METHOD] /api/v1/[resource]

**Purpose:** [one sentence — what this call enables]
**PRD traceability:** FR §[X.Y], Journey: [journey name], Step [N]

**Request:**
\`\`\`json
{
  "field": "type — description"
}
\`\`\`

**Response (200):**
\`\`\`json
{
  "field": "type — description"
}
\`\`\`

**Error responses:**
| Code | Condition | Response body |
|------|-----------|---------------|
| 400 | [validation failure] | `{ "error": "..." }` |
| 401 | [unauthenticated] | `{ "error": "Unauthorised" }` |
| 404 | [resource not found] | `{ "error": "..." }` |

**Auth:** [Bearer token | API key | None]
**Rate limit:** [if NFR specifies one]
**Latency target:** [from NFR — e.g. p95 < 200ms]
```

## 4 — Document key decisions

For each significant architectural choice, write an ADR-lite:

```markdown
### Decision [N]: [Short title]

**Context:** [what situation forced this decision]
**Options considered:**
1. [Option A] — [trade-off]
2. [Option B] — [trade-off]

**Decision:** [Option chosen]
**Rationale:** [why this option, tied to PRD NFRs or success metrics]
**Consequences:** [what this makes easier or harder]
**PRD traceability:** [NFR or requirement it serves]
```

Minimum 3 decisions required. Trivial decisions (framework choice, naming conventions) do not count.

## 5 — Flag open technical risks

List any requirement in the PRD that:
- Cannot be met within the stated NFR constraints without further investigation
- Depends on a third-party API or service with unknown SLA
- Conflicts with an existing data model or API in `docs/specs/`
- Would require a migration of existing data

Format each risk as:

```markdown
**Risk [N]:** [Short title]
- **Severity:** high | medium | low
- **PRD requirement at risk:** §[X.Y]
- **Description:** [what might go wrong]
- **Proposed resolution:** [investigation needed, spike story, or accepted risk]
- **Owner:** [Winston | John | Amelia]
```

Risks are not blockers — they are flags. The Implementation Readiness gate will determine whether they block Phase 04.

## 6 — Validate coverage

Before marking complete, verify:

- [ ] Every PRD functional requirement has at least one corresponding entity or endpoint
- [ ] Every user journey step that writes or reads data has a corresponding API contract
- [ ] Every NFR (latency, throughput, consistency) is addressed in at least one decision
- [ ] No entity or endpoint exists without a PRD trace (scope creep check)

## 7 — Write output

Write the complete document to `tools/bmm/output/architecture-decisions.md`:

```markdown
---
title: "[Initiative] — Architecture Alignment"
date: [YYYY-MM-DD]
status: draft
bmm_phase: 03
prd_source: "tools/bmm/output/prds/final-prd.md"
stepsCompleted: []
---

# [Initiative] — Architecture Alignment

## Context Summary
[2–3 sentences: what is being built, what are the key technical constraints from the PRD]

## Data Model
[Entity definitions]

## API Contracts
[Endpoint definitions]

## Key Decisions
[ADR-lite entries]

## Open Technical Risks
[Risk entries]

## Coverage Checklist
[Completed checklist from step 6]
```

## Output

`tools/bmm/output/architecture-decisions.md` — data model + API contracts + decisions + risks.

**In orchestrated mode:** Winston runs sequentially after Phase 02 is locked. John and Sally are available for clarification queries but do not re-open the PRD. Output feeds the Implementation Readiness check directly.

## Scope rules (strictly enforced)

- **In scope:** data entities, relationships, API endpoints, auth patterns, indexing strategy, integration contracts
- **Out of scope:** infrastructure (hosting, CI/CD, containers), frontend implementation, test strategy, observability setup
- **Escalate to John** if a functional requirement is ambiguous enough to affect the data model
- **Escalate to Sally** if a journey step implies a data interaction that isn't documented in the PRD
