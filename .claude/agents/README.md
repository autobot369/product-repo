# Agent Architecture
> **Status:** Active | **Last Updated:** 2026-03-27

This document describes the agent roster, interaction model, and operational constraints for the BMM workflow system in this repository.

---

## Core Agent Registry

| Agent ID | File | Persona | Purpose | Primary Model | System Prompt Snippet |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `AG-PM` | `pm.md` | John | PRD creation, requirements discovery, stakeholder alignment | claude-sonnet-4-6 | "Prioritise everything with RICE scoring... Every engagement ends at Ready for Dev" |
| `AG-ANALYST` | `analyst.md` | Mary | Market research, competitive analysis, domain expertise, product briefs | claude-sonnet-4-6 | "Apply Porter's Five Forces... Ground all findings in verifiable evidence. Cite sources." |
| `AG-ARCH` | `architect.md` | Winston | System design, API contracts, technical trade-offs, ADRs | claude-sonnet-4-6 | "API-first, always: every feature must be designed as an API contract before any UI work begins" |
| `AG-UX` | `ux-designer.md` | Sally | User journey mapping, interaction design, UX specs | claude-sonnet-4-6 | "Discovery first: users cannot buy what they cannot find... mobile-first, performance-aware" |
| `AG-SM` | `sm.md` | Bob | Sprint planning, story preparation, agile ceremonies, backlog management | claude-sonnet-4-6 | "Servant leader... crisp and checklist-driven. Zero tolerance for ambiguity." |

---

## Interaction Logic

### Handover Chain

Agents operate in a sequential handover pipeline driven by the PM Execution Workflow (`tools/bmm/workflows/pm-execution.yaml`):

```
AG-ANALYST  →  AG-PM  →  AG-UX  →  AG-ARCH  →  AG-SM
  (brief)     (PRD)    (UX spec)  (arch ADR) (stories)
```

| From | To | Handover Artifact | Location |
| :--- | :--- | :--- | :--- |
| `AG-ANALYST` | `AG-PM` | Product Brief | `tools/bmm/output/briefs/` |
| `AG-PM` | `AG-UX` | Validated PRD | `tools/bmm/output/prds/` |
| `AG-PM` / `AG-UX` | `AG-ARCH` | PRD + UX Spec | `tools/bmm/output/prds/` |
| `AG-ARCH` | `AG-SM` | Architecture Doc + PRD | `tools/bmm/output/` |
| `AG-SM` | *(handoff to dev team)* | Context Story file | `tools/bmm/output/stories/` |

### Multi-Agent Collaboration (Party Mode)

All agents support **Party Mode** (`[PM]` menu item), which spawns a multi-agent roundtable discussion. The workflow engine (`tools/bmm/core/workflow.xml`) orchestrates turn order and collects outputs. Party Mode is the primary mechanism for cross-agent critique before stories are written.

### Knowledge / RAG Source

All agents read from `docs/` as their shared knowledge base (configured in `tools/bmm/config.yaml` as `project_knowledge`). Agents query existing PRDs, research documents, and user journeys for context before generating output. Generated artifacts land in `tools/bmm/output/` and are committed to `docs/` selectively once reviewed.

### Workflow Engine

The BMAD workflow engine (`tools/bmm/core/workflow.xml`) is the runtime OS for multi-step workflows. Agents invoke it via the `workflow` handler when processing `.yaml` workflow files. The `exec` handler is used for single-file `.md` playbooks.

---

## Constraints

### Model
- All agents default to **`claude-sonnet-4-6`** (configured in `tools/bmm/config.yaml` → `primary_model`).
- Agents do not pin their own model — the ambient Claude session model is used unless overridden in config.

### Privacy
- No PII should be included in any document committed to `docs/` — these files are git-tracked and potentially published via MkDocs.
- Research outputs in `tools/bmm/output/` are gitignored by default; review before committing.
- Agents do not transmit data to external endpoints independently — all external calls go through the user's Claude session.

### Operational
- Agents are **synchronous and interactive** — designed for human-in-the-loop PM sessions, not autonomous pipelines.
- No latency SLA; response time depends on model and context size.
- Each agent must load `tools/bmm/config.yaml` before any output — failure to load config is a hard stop.
- Agents do not execute menu items automatically; all actions require explicit user selection.

---

## Usage

```
Use @.claude/agents/pm.md — write a PRD for the new checkout feature.
Use @.claude/agents/analyst.md — run market research on loyalty mechanics.
```

## See also

- [.claude/skills/](../skills/README.md) — task-scoped playbooks Claude executes (slash commands)
- [tools/bmm/](../../tools/bmm/README.md) — full PM workflow engine powered by these agents
- [tools/bmm/config.yaml](../../tools/bmm/config.yaml) — model, language, and path configuration
