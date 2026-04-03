# Claude.md — System Prompt for Product Management Repository

This file provides guidance to Claude Code (claude.ai/code) when working in this repository.

## Repository Structure

```
.claude/                    # AI-specific configurations
├── claude.md               # This file — system prompt for the repo
├── agents/                 # Role personas (pm, analyst, architect, ux-designer, sm, dev, qa)
└── skills/                 # Task-scoped playbooks (create-prd, user-stories, etc.)

docs/                       # Product Documentation (MkDocs source) — DEFAULT KNOWLEDGE BASE
├── index.md                # Homepage
├── PRDs/                   # Product Requirement Documents
├── research/               # Research documents
├── user-journeys/          # UX flows mapped by funnel stage
│   ├── Front_Funnel/
│   ├── Mid_Funnel/
│   ├── Bottom_Funnel/
│   └── Loyalty/
├── product-log/            # Year-grouped PRD/research index by funnel
└── specs/                  # Technical specifications

tools/                      # Scripts and internal utilities
├── bmm/                    # BMM workflow engine (BMAD Method v6 — PM-scoped)
│   ├── config.yaml         # BMM config: project_knowledge=docs/, output=tools/bmm/output/
│   ├── core/               # Workflow engine + party-mode/brainstorming workflows
│   │   ├── workflow.xml    # BMAD workflow execution engine
│   │   └── workflows/      # party-mode, brainstorming, advanced-elicitation
│   ├── tasks/              # Shared tasks (remote-context-discovery, remote-output-push)
│   ├── teams/              # Agent team bundles
│   ├── output/             # Generated artifacts (gitignored — commit selectively)
│   │   ├── briefs/
│   │   ├── prds/
│   │   ├── epics/
│   │   ├── stories/
│   │   └── research/
│   └── workflows/
│       ├── pm-execution.yaml           # PM concept-to-story workflow
│       ├── 1-analysis/                 # create-product-brief, research
│       ├── 2-plan-workflows/           # create-prd, create-ux-design
│       ├── 3-solutioning/              # create-architecture, create-epics-and-stories
│       ├── 4-implementation/           # create-story, sprint-planning/status, retrospective
│       └── quick-spec/
├── confluence-migration/   # Confluence → Markdown migration pipeline
├── jira-monitor/           # Sprint/release/demand reporting → Confluence
└── pm-workers/             # Claude-powered PM agents (create-prd, user-stories, etc.)

tests/                      # E2E, integration, and unit tests
README.md
mkdocs.yml
```

## Commands

Activate the virtual environment first:
```bash
source .venv/bin/activate
```

**Serve locally** (with live reload):
```bash
mkdocs serve
```

**Build static site**:
```bash
mkdocs build
```

**Deploy to GitHub Pages**:
```bash
mkdocs gh-deploy
```

## Content Architecture

- `docs/user-journeys/` — Funnel-stage docs (Front → Mid → Bottom → Loyalty)
- `docs/PRDs/` — Product Requirement Documents per feature/initiative
- `docs/specs/` — Technical and functional specifications
- Navigation is driven by `mkdocs.yml`; add new sections there when adding top-level directories
- The `tags` plugin enables cross-linking content across sections
- The Material theme supports [admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/), [tabs](https://squidfunk.github.io/mkdocs-material/reference/content-tabs/), and other enhanced Markdown via `pymdownx` extensions

## Adding Content

- **PRDs**: Place in `docs/PRDs/` and add to `mkdocs.yml` nav
- **User journeys / funnel docs**: Place in `docs/user-journeys/<Funnel>/`
- **Specs**: Place in `docs/specs/`
- **Experiments**: Add definitions and results in `experiments/`
- **Scripts / utilities**: Place in `tools/`
- **Tests**: Place in `tests/`

## AI Agent Roles

Specialized agent instructions live in `.claude/agents/`. Each file describes context and constraints for a specific role:

| Agent | Persona | Best for |
|---|---|---|
| `pm.md` | Optimus Prime | PRD creation, requirements, stakeholder alignment. **Pipeline orchestrator** for the full PM execution workflow |
| `analyst.md` | Bumblebee | Market research, competitive analysis, product briefs |
| `architect.md` | Wheeljack | Tech feasibility, API/data model decisions, ADRs |
| `ux-designer.md` | Arcee | User journey mapping, interaction design (inline into PRD) |
| `sm.md` | Ironhide | Sprint planning, Gherkin story authoring, Jira push |

**Invoke an agent:**
```
Use @.claude/agents/pm.md — run the full PM execution workflow
Use @.claude/agents/analyst.md — run market research on [topic]
```

## Skills (Unified Execution Layer)

Skills are the canonical execution layer — step-by-step playbooks invoked via `/command`. Every skill declares its BMM phase, agent owner, output contract, and handoff signals.

| Skill | Command | Agent | BMM Phase |
|---|---|---|---|
| `create-product-brief.md` | `/create-product-brief` | Optimus Prime (pm) | 01 — Context Discovery |
| `market-research.md` | `/market-research` | Bumblebee (analyst) | 01 — Context Discovery |
| `create-prd.md` | `/create-prd` | Optimus Prime (pm) | 02 — Solutioning Sprint |
| `ux-journeys.md` | `/ux-journeys` | Arcee (ux-designer) | 02 — Solutioning Sprint |
| `create-architecture.md` | `/create-architecture` | Wheeljack (architect) | 03 — Architecture |
| `confluence-user-stories.md` | `/confluence-user-stories` | Optimus Prime (pm) | 04 — Backlog |
| `user-stories.md` | `/user-stories` | Ironhide (sm) | 04 — Backlog |

Skills can be run standalone or as part of the orchestrated pipeline. See `.claude/skills/README.md` for the full capability matrix.

## BMM Workflow Engine

The `tools/bmm/` directory contains a PM-scoped BMAD Method workflow engine (v2.0).

**Config:** `tools/bmm/config.yaml`
- `project_knowledge`: `docs/` — agents read existing PRDs, research, and user journeys as context
- `output_folder`: `tools/bmm/output/` — all generated artifacts land here before optional Confluence publish

**Run the full concept-to-story pipeline (recommended):**
```
Use @.claude/agents/pm.md
→ Select: [RW] Run PM Execution Workflow
```

Optimus Prime (pm) acts as orchestrator — he embodies each agent in sequence, runs the relevant skill per phase, writes handoff context between phases, and facilitates party-mode gates. No manual agent switching required.

**Or run individual skills:**
```
/create-product-brief   Initiative: [name]  Idea: [description]
/market-research        Topic: [area]
/create-prd             Initiative: [name]  ...
/ux-journeys            PRD: tools/bmm/output/prds/final-prd.md
/create-architecture    PRD: tools/bmm/output/prds/final-prd.md
/user-stories           PRD: [url]  Jira project: [key]
```

**Pipeline phases and gates:**

```
Phase 01 — Context Discovery
  Optimus Prime (/create-product-brief) + Bumblebee (/market-research)
  ↓ Gate: Strategic Alignment [party-mode: Optimus Prime + Bumblebee + Wheeljack]

Phase 02 — Solutioning Sprint
  Optimus Prime (/create-prd) + Arcee (/ux-journeys inline)
  ↓ Gate: Technical Readiness [party-mode: Optimus Prime + Arcee + Wheeljack]

Phase 03 — Architecture
  Wheeljack (/create-architecture) → automated readiness check
  ↓ Gate: Implementation Readiness [auto-pass or targeted party-mode]

Phase 04 — One-Shot Backlog
  Optimus Prime (/confluence-user-stories intent) → Ironhide (/user-stories Gherkin + Jira)
  ↓ Post-process: Gherkin validator → user approves publish
```

**Output structure:**
```
tools/bmm/output/
├── briefs/                    ← product brief (phase 01)
├── research/                  ← market research findings (phase 01)
├── prds/final-prd.md          ← PRD + inline UX journeys (phase 02)
├── architecture-decisions.md  ← data model + API contracts (phase 03)
├── readiness-report.md        ← implementation readiness check (phase 03)
├── stories/                   ← Gherkin user stories (phase 04)
├── gherkin-validation-report.md
├── handoff-01.md              ← phase boundary context (written by orchestrator)
├── handoff-02.md
└── handoff-03.md
```

Generated files are gitignored by default — commit them to `docs/PRDs/` manually once reviewed.
