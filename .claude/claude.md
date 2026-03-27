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
| `pm.md` | John | PRD creation, requirements, stakeholder alignment |
| `analyst.md` | Mary | Market research, competitive analysis |
| `architect.md` | Winston | Tech feasibility, API/data model decisions |
| `ux-designer.md` | Sally | User journey mapping, interaction design |
| `sm.md` | Bob | Sprint planning, story prep, retrospectives |
| `dev.md` | Amelia | Story-level specs, implementation notes |
| `qa.md` | Quinn | Test plans, acceptance criteria review |

**Invoke an agent:**
```
Use @.claude/agents/pm.md — create a PRD for [feature]
Use @.claude/agents/analyst.md — run market research on [topic]
```

**Skills** (task playbooks) live in `.claude/skills/` — invoke via `/create-prd`, `/user-stories`, etc.

## BMM Workflow Engine

The `tools/bmm/` directory contains a PM-scoped BMAD Method workflow engine.

**Config:** `tools/bmm/config.yaml`
- `project_knowledge`: `docs/` — agents read existing PRDs, research, and user journeys as context
- `output_folder`: `tools/bmm/output/` — all generated artifacts land here before optional Confluence publish

**Run the full concept-to-story flow:**
```
Use @.claude/agents/pm.md
→ Select: Run PM Execution Workflow
→ Workflow: tools/bmm/workflows/pm-execution.yaml
```

**Or run individual workflows:**
```
Use @.claude/agents/pm.md — run create-prd workflow
Use @.claude/agents/analyst.md — run market research on [topic]
Use @.claude/agents/sm.md — run sprint planning
```

**Output structure:**
```
tools/bmm/output/
├── briefs/        ← product brief (phase 01)
├── research/      ← market/domain research (phase 01)
├── prds/          ← final PRD (phase 02)
├── epics/         ← epic breakdowns (phase 04)
└── stories/       ← Gherkin user stories (phase 04)
```

Generated files are gitignored by default — commit them to `docs/PRDs/` manually once reviewed.
