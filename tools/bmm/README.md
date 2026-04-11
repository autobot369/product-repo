# BMM — PM Workflow Engine

BMM is a PM-scoped workflow engine built on the [BMAD Method v6](https://github.com/bmad-method). It provides structured, agent-driven workflows that take a product idea from initial concept through to dev-ready Gherkin user stories.

**The engine is installed globally at `~/.claude/bmm/`.** This directory (`tools/bmm/`) holds only the per-repo configuration and generated output.

---

## Quick Start

```
Use @~/.claude/agents/pm.md → [RW] Run PM Execution Workflow
```

The agent loads `tools/bmm/config.yaml` on activation, greets you by name, and presents its menu. All navigation is menu-driven — no manual file execution needed.

---

## Configuration

**File:** [config.yaml](config.yaml) — the only BMM file that lives in this repo.

| Field | Purpose |
|-------|---------|
| `project_name` | Used in output file headers |
| `user_name` | Personalises agent greetings |
| `user_skill_level` | Calibrates agent response verbosity (`beginner` / `intermediate` / `expert`) |
| `communication_language` | Language for all agent output |
| `primary_model` | Claude model used by all agents |
| `project_knowledge` | Root knowledge base (`{project-root}/docs`) |
| `output_folder` | Where generated artefacts land (`{project-root}/tools/bmm/output`) |
| `docs_prds` / `docs_research` / `docs_user_journeys` / `docs_specs` | Sub-folder context paths for targeted agent reads |
| `prd_intake_mode` | `strategic-core` (one-pass) or `step-by-step` (guided) |

The workflow engine path, agent file paths, and workflow paths are all resolved from `~/.claude/` — not from this config.

---

## Agents

All agents live globally at `~/.claude/agents/` and are available in any repo. Each agent loads `tools/bmm/config.yaml` on activation.

| Agent | Persona | Role | Key menu commands |
|-------|---------|------|-------------------|
| `pm.md` | Optimus Prime | Pipeline orchestrator — runs the full concept-to-story workflow | `[RW]` Run workflow, `[CP]` Create PRD, `[VP]` Validate PRD, `[EP]` Edit PRD, `[PB]` Product Brief |
| `analyst.md` | Bumblebee | Market research, competitive analysis, product briefs | `[MR]` Market Research, `[DR]` Domain Research, `[CB]` Create Brief |
| `architect.md` | Wheeljack | Data model, API contracts, ADRs, feasibility | `[CA]` Create Architecture, `[IR]` Implementation Readiness |
| `ux-designer.md` | Arcee | User journey mapping, inline UX into PRD | `[UJ]` Map UX Journeys, `[CU]` Create UX |
| `sm.md` | Ironhide | Gherkin story authoring, sprint planning, Jira push | `[US]` User Stories, `[SP]` Sprint Planning, `[CS]` Context Story, `[ER]` Retrospective |

**Invoke an agent:**
```
Use @~/.claude/agents/pm.md
Use @~/.claude/agents/analyst.md
Use @~/.claude/agents/sm.md
```

---

## Skills

All skills live globally at `~/.claude/skills/` and are invoked as slash commands.

| Command | Agent | Phase | Output |
|---------|-------|-------|--------|
| `/create-product-brief` | Optimus Prime | 01 | `tools/bmm/output/briefs/product-brief.md` |
| `/market-research` | Bumblebee | 01 | `tools/bmm/output/research/research-findings.md` |
| `/create-prd` | Optimus Prime | 02 | `tools/bmm/output/prds/final-prd.md` |
| `/ux-journeys` | Arcee | 02 | Inline into `final-prd.md` |
| `/create-architecture` | Wheeljack | 03 | `tools/bmm/output/architecture-decisions.md` |
| `/confluence-user-stories` | Optimus Prime | 04 | `tools/bmm/output/stories/story-intent.md` |
| `/user-stories` | Ironhide | 04 | `tools/bmm/output/stories/` + Jira |

---

## Full Concept-to-Story Pipeline

The flagship workflow runs a complete concept → research → PRD → architecture → stories pipeline, orchestrated by Optimus Prime across all agents with three quality gates.

**Trigger:**
```
Use @~/.claude/agents/pm.md → [RW] Run PM Execution Workflow
```

### Phases

```
Phase 01 — Context Discovery          [Optimus Prime + Bumblebee]
  ├── /create-product-brief           → output/briefs/product-brief.md
  ├── /market-research                → output/research/research-findings.md
  └── Gate: Strategic Alignment       [party-mode: Optimus Prime + Bumblebee + Wheeljack]
      Outcome: go | amend-brief | no-go

Phase 02 — Solutioning Sprint         [Optimus Prime + Arcee]
  ├── /create-prd                     → output/prds/final-prd.md
  ├── /ux-journeys                    → inline into final-prd.md
  └── Gate: Technical Readiness       [party-mode: Optimus Prime + Arcee + Wheeljack]
      Outcome: go | open-items | no-go

Phase 03 — Architecture               [Wheeljack]
  ├── /create-architecture            → output/architecture-decisions.md
  ├── Readiness check (automated)
  └── Gate: Implementation Readiness  [auto-pass or party-mode: Optimus Prime + Wheeljack]
      Outcome: ready | gaps-found

Phase 04 — One-Shot Backlog           [Optimus Prime + Ironhide]
  ├── /confluence-user-stories        → output/stories/story-intent.md
  ├── /user-stories                   → output/stories/*.md + Jira push
  └── Post-process: Gherkin validator → user approves publish
```

---

## Individual Workflows

Run any workflow standalone without the full pipeline:

### Phase 1 — Analysis

| Workflow | Invoke via |
|----------|-----------|
| Product Brief | `/create-product-brief` or `@~/.claude/agents/pm.md → [PB]` |
| Market Research | `/market-research` or `@~/.claude/agents/analyst.md → [MR]` |
| Domain Research | `@~/.claude/agents/analyst.md → [DR]` |
| Technical Research | `@~/.claude/agents/analyst.md → [TR]` |

### Phase 2 — Planning

| Workflow | Invoke via |
|----------|-----------|
| Create PRD | `/create-prd` or `@~/.claude/agents/pm.md → [CP]` |
| Validate PRD | `@~/.claude/agents/pm.md → [VP]` |
| Edit PRD | `@~/.claude/agents/pm.md → [EP]` |
| UX Journeys | `/ux-journeys` or `@~/.claude/agents/ux-designer.md → [UJ]` |

### Phase 3 — Architecture

| Workflow | Invoke via |
|----------|-----------|
| Create Architecture | `/create-architecture` or `@~/.claude/agents/architect.md → [CA]` |
| Implementation Readiness | `@~/.claude/agents/pm.md → [IR]` or `@~/.claude/agents/architect.md → [IR]` |

### Phase 4 — Backlog

| Workflow | Invoke via |
|----------|-----------|
| Story Intent | `/confluence-user-stories` |
| Gherkin Stories + Jira | `/user-stories` or `@~/.claude/agents/sm.md → [US]` |
| Sprint Planning | `@~/.claude/agents/sm.md → [SP]` |
| Context Story Prep | `@~/.claude/agents/sm.md → [CS]` |
| Retrospective | `@~/.claude/agents/sm.md → [ER]` |
| Course Correction | `@~/.claude/agents/pm.md → [CC]` or `@~/.claude/agents/sm.md → [CC]` |

### Quick Spec

For small changes that don't need the full pipeline:

```
Use @~/.claude/agents/pm.md — run quick spec for [feature]
```

---

## Output Structure

```
tools/bmm/output/               ← gitignored — commit selectively to docs/PRDs/
├── briefs/
│   └── product-brief.md        ← Phase 01
├── research/
│   └── research-findings.md    ← Phase 01
├── prds/
│   └── final-prd.md            ← Phase 02 (includes inline UX journeys)
├── architecture-decisions.md   ← Phase 03
├── stories/
│   ├── story-intent.md         ← Phase 04 (Optimus Prime handoff to Ironhide)
│   └── *.md                    ← Phase 04 (Gherkin stories)
├── handoff-01.md               ← Phase boundary context (written by orchestrator)
├── handoff-02.md
└── handoff-03.md
```

> Outputs are gitignored by default. Once reviewed, move approved docs to `docs/PRDs/` and add to `mkdocs.yml` nav for publication.

---

## Directory Structure (this repo)

```
tools/bmm/
├── config.yaml     ← Per-repo configuration (committed) — only file that lives here
├── README.md       ← This file
└── output/         ← Generated artefacts (gitignored)
```

The workflow engine, workflows, core, tasks, teams, and data directories all live globally at `~/.claude/bmm/` and are shared across all repos.

---

## Using BMM in a New Repo

1. Create `tools/bmm/config.yaml` with your project-specific settings (copy from this file as a template)
2. Add `tools/bmm/output/` to `.gitignore`
3. Invoke any agent or skill — the global engine at `~/.claude/bmm/` handles the rest

See `~/.claude/CLAUDE.md` for the full global setup reference.

---

[Back to tools/](../README.md)
