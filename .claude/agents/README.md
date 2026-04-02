# Agent Architecture
> **Status:** Active | **Last Updated:** 2026-04-02

This document describes the agent roster, orchestration model, gate protocol, and operational constraints for the BMM v2.0 workflow system.

---

## Core Agent Registry

| Agent ID | File | Persona | Role in Pipeline | Primary Model |
| :--- | :--- | :--- | :--- | :--- |
| `AG-PM` | `pm.md` | John | **Pipeline Orchestrator** — owns all phases, embodies other agents in sequence, runs gates | claude-sonnet-4-6 |
| `AG-ANALYST` | `analyst.md` | Mary | Phase 01 — market research, competitive analysis, product briefs | claude-sonnet-4-6 |
| `AG-UX` | `ux-designer.md` | Sally | Phase 02 — user journey mapping, inline UX into PRD | claude-sonnet-4-6 |
| `AG-ARCH` | `architect.md` | Winston | Phase 03 — data model, API contracts, ADRs, gate challenger | claude-sonnet-4-6 |
| `AG-SM` | `sm.md` | Bob | Phase 04 — Gherkin story authoring, Jira push, Gherkin validation | claude-sonnet-4-6 |
| `AG-DEV` | `dev.md` | Amelia | Standalone — story-level specs, implementation notes | claude-sonnet-4-6 |
| `AG-QA` | `qa.md` | Quinn | Standalone — test plans, acceptance criteria review | claude-sonnet-4-6 |

---

## Orchestration Model

John (AG-PM) is the **pipeline orchestrator**. When the user selects `[RW] Run PM Execution Workflow`, John:

1. Loads `tools/bmm/workflows/pm-execution.yaml` and reads all phases, gates, and skill bindings
2. Executes each phase by **embodying the relevant agent** — loading their `.md` file and adopting their persona fully for the duration of that step
3. Announces every agent switch: `"— Switching to [Name] ([role]) for [step] —"`
4. Writes a handoff file (`tools/bmm/output/handoff-{N}.md`) at the end of every phase
5. Checks the output contract for each phase before launching a gate
6. Facilitates party-mode gates with the declared participants
7. Resumes mid-pipeline if handoff files already exist (no restart from Phase 01)

**Entry point:**
```
Use @.claude/agents/pm.md → [RW] Run PM Execution Workflow
```

---

## Pipeline: Agent × Phase × Skill

```
Phase 01 — Context Discovery
  AG-ANALYST (Mary)   → /market-research        → research/research-findings.md
  AG-PM (John)        → /create-product-brief   → briefs/product-brief.md
  ──────────────────────────────────────────────────────────────
  Gate: Strategic Alignment  [party-mode: John + Mary + Winston]
  Outcome: go | amend-brief | no-go

Phase 02 — Solutioning Sprint
  AG-PM (John)        → /create-prd             → prds/final-prd.md
  AG-UX (Sally)       → /ux-journeys            → inline into final-prd.md
  PRD validator runs automatically before gate
  ──────────────────────────────────────────────────────────────
  Gate: Technical Readiness  [party-mode: John + Sally + Winston]
  Outcome: go | open-items | no-go

Phase 03 — Architecture
  AG-ARCH (Winston)   → /create-architecture    → architecture-decisions.md
  Readiness check runs automatically
  ──────────────────────────────────────────────────────────────
  Gate: Implementation Readiness  [auto-pass or party-mode: John + Winston]
  Outcome: ready | gaps-found (targeted Phase 02 return)

Phase 04 — One-Shot Backlog
  AG-PM (John)        → /confluence-user-stories → stories/story-intent.md
  AG-SM (Bob)         → /user-stories            → stories/*.md + Jira
  Gherkin validator runs automatically
  ──────────────────────────────────────────────────────────────
  Gate: Backlog Complete  [automated]
  Outcome: complete | validator-failures (Bob re-runs failing stories only)
```

---

## Handover Chain

Phase boundary context is carried via handoff files — not verbal context or assumptions.

| Phase end | Handoff file | Written by | Read by |
| :--- | :--- | :--- | :--- |
| Phase 01 | `tools/bmm/output/handoff-01.md` | John (PM) | John (PM) at Phase 02 start |
| Phase 02 | `tools/bmm/output/handoff-02.md` | John (PM) | Winston (Arch) at Phase 03 start |
| Phase 03 | `tools/bmm/output/handoff-03.md` | Winston (Arch) | John (PM) at Phase 04 start |

Each handoff records: outputs produced, gate outcome + rationale, key decisions, assumptions to carry forward, items not to re-open, and orchestrator signals (boolean flags checked by the pipeline).

Template: `tools/bmm/data/handoff-template.md`

---

## Gate Protocol

All phase gates use **Party Mode** (`tools/bmm/core/workflows/party-mode/workflow.md`) as the mechanism — a structured multi-agent discussion with a declared agenda and typed outcomes.

| Gate | Mechanism | Participants | Outcome options |
| :--- | :--- | :--- | :--- |
| Strategic Alignment (01→02) | Party Mode | John + Mary + Winston | go / amend-brief / no-go |
| Technical Readiness (02→03) | Party Mode | John + Sally + Winston | go / open-items / no-go |
| Implementation Readiness (03→04) | Auto + optional Party Mode | John + Winston | ready / gaps-found |
| Backlog Complete (04→publish) | Automated | — | complete / validator-failures |

Gate rules:
- Output contract must be satisfied before a gate launches
- User must confirm gate outcome before the pipeline advances
- `no-go` terminates the workflow and writes a decision log
- `amend` / `open-items` / `gaps-found` return to the **specific flagged step only**, not the phase start

---

## Multi-Agent Collaboration (Party Mode)

Party Mode (`[PM]` menu item on any agent) spawns a structured multi-agent discussion. The orchestrator loads each participant's agent file and embodies them in turn, maintaining strict persona consistency.

**Gate use:** John launches party mode at each phase gate with the declared participants and agenda.

**Ad-hoc use:** Any agent can invoke `[PM]` for open-ended brainstorming or cross-agent critique outside the pipeline.

---

## Knowledge / RAG Sources

All agents read from two sources before generating output:

1. **`docs/`** — local MkDocs knowledge base (PRDs, research, user journeys, specs) — configured as `project_knowledge` in `tools/bmm/config.yaml`
2. **Confluence** — live space search via Atlassian MCP — run by `tools/bmm/tasks/remote-context-discovery.md` at the start of each phase

Generated artifacts land in `tools/bmm/output/` (gitignored) and are committed to `docs/` selectively once reviewed.

---

## Constraints

### Model
- All agents default to **`claude-sonnet-4-6`** (configured in `tools/bmm/config.yaml` → `primary_model`).
- Model is not pinned per-agent — the ambient Claude session model is used unless overridden in config.

### Privacy
- No PII in any document committed to `docs/` — these files are git-tracked and published via MkDocs.
- Research and story outputs in `tools/bmm/output/` are gitignored by default.
- Agents do not transmit data to external endpoints independently — all external calls go through the user's Claude session.

### Operational
- Agents are **synchronous and interactive** — human-in-the-loop at every gate and approval step.
- Each agent must load `tools/bmm/config.yaml` before any output — failure to load config is a hard stop.
- Agents do not execute menu items automatically; all actions require explicit user selection.
- Skills take precedence over BMM workflow files when both are present — skills are the canonical layer.

---

## Usage

```
# Full pipeline (recommended)
Use @.claude/agents/pm.md → [RW] Run PM Execution Workflow

# Standalone agent
Use @.claude/agents/pm.md — create a PRD for [feature]
Use @.claude/agents/analyst.md — run market research on [topic]
Use @.claude/agents/architect.md — review architecture for [system]

# Standalone skill
/create-product-brief   Initiative: Mobile Checkout  Idea: reduce drop-off at payment
/market-research        Topic: AI personalisation in retail 2026
/create-prd             Initiative: One-tap Checkout  ...
```

## See also

- [.claude/skills/README.md](../skills/README.md) — full skill registry and capability matrix
- [tools/bmm/workflows/pm-execution.yaml](../../tools/bmm/workflows/pm-execution.yaml) — full pipeline definition with gates and output contracts
- [tools/bmm/data/handoff-template.md](../../tools/bmm/data/handoff-template.md) — phase handoff contract template
- [tools/bmm/config.yaml](../../tools/bmm/config.yaml) — model, language, and path configuration
