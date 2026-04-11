# Skill & Capability Matrix
> **Status:** Active | **Last Updated:** 2026-04-02

Slash-command skills are the **canonical execution layer** for this PM workspace. Every skill is a step-by-step playbook that declares its BMM pipeline phase, agent owner, output file contract, and handoff signals. Skills can be run standalone or as part of the orchestrated PM Execution Workflow.

---

## Skill Registry

| Skill | Command | Agent | BMM Phase | Output |
| :--- | :--- | :--- | :--- | :--- |
| `create-product-brief.md` | `/create-product-brief` | Optimus Prime (pm) | 01 — Context Discovery | `tools/bmm/output/briefs/product-brief.md` |
| `market-research.md` | `/market-research` | Bumblebee (analyst) | 01 — Context Discovery | `tools/bmm/output/research/research-findings.md` |
| `create-prd.md` | `/create-prd` | Optimus Prime (pm) | 02 — Solutioning Sprint | `tools/bmm/output/prds/final-prd.md` |
| `ux-journeys.md` | `/ux-journeys` | Arcee (ux-designer) | 02 — Solutioning Sprint | Inline into `final-prd.md` |
| `create-architecture.md` | `/create-architecture` | Wheeljack (architect) | 03 — Architecture | `tools/bmm/output/architecture-decisions.md` |
| `confluence-user-stories.md` | `/confluence-user-stories` | Optimus Prime (pm) | 04 — Backlog | `tools/bmm/output/stories/story-intent.md` |
| `user-stories.md` | `/user-stories` | Ironhide (sm) | 04 — Backlog | `tools/bmm/output/stories/` |

---

## Pipeline flow

```
Phase 01 — Context Discovery
  /create-product-brief  (Optimus Prime)   →  briefs/product-brief.md
  /market-research       (Bumblebee)   →  research/research-findings.md
  ↓ Gate: Strategic Alignment [party-mode: Optimus Prime + Bumblebee + Wheeljack]

Phase 02 — Solutioning Sprint
  /create-prd            (Optimus Prime)   →  prds/final-prd.md
  /ux-journeys           (Arcee)  →  embedded into final-prd.md
  ↓ Gate: Technical Readiness [party-mode: Optimus Prime + Arcee + Wheeljack]

Phase 03 — Architecture
  /create-architecture   (Wheeljack) →  architecture-decisions.md
  ↓ Gate: Implementation Readiness [automated + optional party-mode]

Phase 04 — One-Shot Backlog
  /confluence-user-stories (Optimus Prime) →  stories/story-intent.md
  /user-stories            (Ironhide)  →  stories/*.md + Jira push
  ↓ Post-process: Gherkin validator → user approves publish
```

Run the full pipeline with one command:
```
Use @.claude/agents/pm.md → [RW] Run PM Execution Workflow
```

---

## Product Capabilities (Functional)

### /create-product-brief
- **Description:** Drafts a structured product brief — problem statement, target user, success metrics, and scope. Seeds the PRD. Skips if a brief already exists.
- **Owner:** AG-PM (Optimus Prime)
- **Standalone invoke:** `Initiative: [name]  Idea: [1–3 sentence description]`
- **Dependencies:** Confluence (search related PRDs and research)

### /market-research
- **Description:** Targeted web + Confluence research producing a structured market report published to Confluence.
- **Owner:** AG-ANALYST (Bumblebee)
- **Standalone invoke:** `Topic: [area]  Markets: US, UK  Depth: full`
- **Dependencies:** Confluence (search, read, create page), WebSearch

### /create-prd
- **Description:** Full PRD authored from brief + research. Reads brief and research findings as primary inputs. Includes NFRs. Runs 12-step validation on completion.
- **Owner:** AG-PM (Optimus Prime)
- **Standalone invoke:** `Initiative: [name]  Business Problem: ...  User Problem: ...  Ideal Solution: ...  Metrics: ...`
- **Dependencies:** Confluence (search, read, create/update page), Jira (epic reference)

### /ux-journeys
- **Description:** Maps user journeys (happy path, failure states, edge cases) and embeds them inline into the PRD's Functional Requirements section. No separate UX doc produced.
- **Owner:** AG-UX (Arcee)
- **Standalone invoke:** `PRD: tools/bmm/output/prds/final-prd.md  Feature: [name]`
- **Dependencies:** Confluence (design system, existing journey pages), `docs/user-journeys/`

### /create-architecture
- **Description:** Defines data model and API contracts for a locked PRD. Scoped to data-model-and-APIs only — no infrastructure. Produces ADR-lite decisions and risk flags.
- **Owner:** AG-ARCH (Wheeljack)
- **Standalone invoke:** `PRD: tools/bmm/output/prds/final-prd.md`
- **Dependencies:** Confluence (existing specs, ADRs), Jira (related technical epics)

### /confluence-user-stories
- **Description:** Scans Confluence space or reads PRD to produce story intent (user story statement + acceptance criteria + PRD trace). Handoff input for /user-stories.
- **Owner:** AG-PM (Optimus Prime)
- **Standalone invoke:** `Space: TEAM  Jira project: SQUAD1  Epic: SQUAD1-100`
- **Dependencies:** Confluence (read pages), Jira (search stories, link epic)

### /user-stories
- **Description:** Converts story intent into full Gherkin stories (Given/When/Then) and pushes to Jira. Auto-selects template (Standard / Technical / Gherkin) per story.
- **Owner:** AG-SM (Ironhide)
- **Standalone invoke:** `PRD: [url]  Jira project: SQUAD1  Epic: SQUAD1-42  Board ID: 7`
- **Dependencies:** Confluence (search, read pages), Jira (create issues, get sprints, assign)

---

## Team Skills (Operational)

| Skill | Lead | Backup | File |
| :--- | :--- | :--- | :--- |
| Product Brief | AG-PM (Optimus Prime) | AG-ANALYST (Bumblebee) | [create-product-brief.md](create-product-brief.md) |
| Market Research | AG-ANALYST (Bumblebee) | AG-PM (Optimus Prime) | [market-research.md](market-research.md) |
| PRD Writing | AG-PM (Optimus Prime) | AG-ANALYST (Bumblebee) | [create-prd.md](create-prd.md) |
| UX Journey Mapping | AG-UX (Arcee) | — | [ux-journeys.md](ux-journeys.md) |
| Architecture Design | AG-ARCH (Wheeljack) | — | [create-architecture.md](create-architecture.md) |
| Story Intent | AG-PM (Optimus Prime) | AG-SM (Ironhide) | [confluence-user-stories.md](confluence-user-stories.md) |
| Gherkin Stories + Jira | AG-SM (Ironhide) | AG-PM (Optimus Prime) | [user-stories.md](user-stories.md) |

---

## Tooling Stack

* **LLM:** claude-sonnet-4-6 — default model for all agents and skills (configured in `tools/bmm/config.yaml`)
* **PM Workflow Engine:** BMM v2.0 (`tools/bmm/workflows/pm-execution.yaml`) — orchestrates the full pipeline via Optimus Prime as orchestrator
* **Gate mechanism:** Party Mode (`tools/bmm/core/workflows/party-mode/`) — multi-agent alignment sessions at phase boundaries
* **Knowledge Base:** `docs/` (MkDocs) + Confluence space (via Atlassian MCP) — agents read both for context
* **Issue Tracking:** Jira (via Atlassian MCP) — story creation, sprint assignment, epic linking
* **Handoff layer:** `tools/bmm/output/handoff-{N}.md` — phase boundary context written by orchestrator, read by next agent

---

## Skill frontmatter spec

Every skill file must declare:

```yaml
---
description:     # ≤30 words
bmm_phase:       # e.g. "02_Solutioning_Sprint" or "standalone"
bmm_step:        # step name in pm-execution.yaml
bmm_agent:       # pm | analyst | ux-designer | architect | sm
bmm_runs:        # standalone_only | standalone_or_orchestrated
output_file:     # path to primary output (or "inline" for embedded outputs)
output_contract: # required_sections, min_counts etc.
handoff_writes:  # list of key/value signals written to handoff file
dependencies:    # external services called
---
```

## Adding a new skill

1. Copy an existing skill as a template
2. Fill in all frontmatter fields including `bmm_phase` and `output_contract`
3. Add the skill to the registry table in this README
4. Add it to the `skills:` block in `tools/bmm/workflows/pm-execution.yaml` if it belongs to the pipeline
5. Add it to the `Team Skills` table in `.claude/agents/README.md`

## See also

- [.claude/agents/README.md](../agents/README.md) — agent registry, handover chain, interaction model
- [tools/bmm/workflows/pm-execution.yaml](../../tools/bmm/workflows/pm-execution.yaml) — full pipeline definition
- [tools/bmm/data/handoff-template.md](../../tools/bmm/data/handoff-template.md) — phase handoff contract template
- [tools/pm-workers/README.md](../../tools/pm-workers/README.md) — CLI runner for programmatic skill execution
