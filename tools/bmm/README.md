# BMM — PM Workflow Engine

BMM is a PM-scoped workflow engine built on the [BMAD Method v6](https://github.com/bmad-method). It provides structured, agent-driven workflows that take a product idea from initial concept through to dev-ready Gherkin user stories.

All agents read from `docs/` as their knowledge base and write outputs to `tools/bmm/output/` before optional Confluence publish.

---

## Quick Start

Invoke any agent via Claude Code:

```
Use @.claude/agents/pm.md
```

The agent loads `tools/bmm/config.yaml` on activation, greets you by name, and presents its menu. All navigation is menu-driven — no manual file execution needed.

---

## Configuration

**File:** [config.yaml](config.yaml)

| Field | Value | Purpose |
|-------|-------|---------|
| `user_name` | `Shiv` | Personalises agent greetings |
| `communication_language` | `English` | Language for all agent output |
| `project_knowledge` | `{project-root}/docs` | Root knowledge base |
| `docs_prds` | `{project-root}/docs/PRDs` | PRD context for agents |
| `docs_research` | `{project-root}/docs/research` | Research context for agents |
| `docs_user_journeys` | `{project-root}/docs/user-journeys` | Journey map context |
| `docs_specs` | `{project-root}/docs/specs` | Spec context for agents |
| `output_folder` | `{project-root}/tools/bmm/output` | Where generated artefacts land |
| `workflow_engine` | `{project-root}/tools/bmm/core/workflow.xml` | Core execution engine |

---

## Agents

Each agent is invoked via its file in `.claude/agents/`. On activation, every agent loads `config.yaml`, greets the user, and presents a numbered menu.

| Agent file | Persona | Role | Key menu commands |
|------------|---------|------|-------------------|
| `pm.md` | John | Product Manager | Create PRD, Validate PRD, Edit PRD, Epics & Stories |
| `analyst.md` | Mary | Market Analyst | Market research, domain research, technical research |
| `architect.md` | Winston | Solutions Architect | Architecture decisions, tech feasibility |
| `ux-designer.md` | Sally | UX Designer | UX design, journey mapping |
| `sm.md` | Bob | Scrum Master | Sprint planning, story context prep, retrospective, course correction |
| `dev.md` | Amelia | Developer | Story implementation notes |
| `qa.md` | Quinn | QA Engineer | Test plans, acceptance criteria review |

**Invoke an agent:**
```
Use @.claude/agents/pm.md
Use @.claude/agents/sm.md
Use @.claude/agents/analyst.md
```

---

## Full Concept-to-Story Flow (PM Execution Workflow)

The flagship workflow runs a complete concept → research → PRD → UX + architecture → epics → stories pipeline, orchestrated across all agents with three quality gates.

**Trigger:**
```
Use @.claude/agents/pm.md
→ Select: Run PM Execution Workflow  (or type "pm-execution")
→ Workflow: tools/bmm/workflows/pm-execution.yaml
```

### Phases

```
Phase 01 — Strategic Analysis        [analyst + pm]
  ├── Brainstorming Session           (First Principles, SCAMPER)
  ├── Market Research                 → output/research-findings.md
  └── Party Mode: Feasibility Gate    (analyst + pm + architect must agree)

Phase 02 — Requirements Definition   [pm + ux-designer]
  ├── Product Brief                   → output/briefs/product-brief.md
  ├── PRD Creation                    → output/prds/final-prd.md
  └── Requirements Gate               (PRD validation — must pass before Phase 03)

Phase 03 — Solutioning & Design      [ux-designer + architect]
  ├── UX Design                       → output/ux-design.md
  ├── Architecture Alignment          → output/architecture-decisions.md
  └── Party Mode: UX ↔ Arch Check     (Sally + Winston + John)

Phase 04 — Backlog Creation          [pm + sm]
  ├── Create Epics                    → output/epics/
  ├── Generate User Stories (Gherkin) → output/stories/
  └── Final Gate: Story ↔ PRD Trace   (readiness report before Jira publish)
```

---

## Individual Workflows

Run any workflow standalone without the full pipeline:

### Phase 1 — Analysis

| Workflow | Agent | Invoke via |
|----------|-------|-----------|
| Create Product Brief | `pm.md` → `[CP]` or analyst | Menu option or direct |
| Market Research | `analyst.md` | `workflow-market-research.md` |
| Domain Research | `analyst.md` | `workflow-domain-research.md` |
| Technical Research | `analyst.md` | `workflow-technical-research.md` |

### Phase 2 — Planning

| Workflow | Agent | Command |
|----------|-------|---------|
| Create PRD | `pm.md` | `[CP]` Create PRD |
| Validate PRD | `pm.md` | `[VP]` Validate PRD |
| Edit PRD | `pm.md` | `[EP]` Edit PRD |
| Create UX Design | `ux-designer.md` | Agent menu |

### Phase 3 — Solutioning

| Workflow | Agent | Command |
|----------|-------|---------|
| Create Architecture | `architect.md` | Agent menu |
| Create Epics & Stories | `pm.md` | `[CE]` Create Epics and Stories |
| Implementation Readiness | `pm.md` | `[IR]` Implementation Readiness |

### Phase 4 — Implementation

| Workflow | Agent | Command |
|----------|-------|---------|
| Sprint Planning | `sm.md` | `[SP]` Sprint Planning |
| Context Story Prep | `sm.md` | `[CS]` Context Story |
| Retrospective | `sm.md` | `[ER]` Epic Retrospective |
| Course Correction | `pm.md` or `sm.md` | `[CC]` Course Correction |

### Quick Spec

For small changes or features that don't need the full pipeline:

```
Use @.claude/agents/pm.md — run quick spec for [feature]
```

Workflow: `tools/bmm/workflows/quick-spec/workflow.md`

---

## Output Structure

```
tools/bmm/output/           ← gitignored — commit selectively to docs/PRDs/
├── briefs/                 ← product-brief.md  (Phase 01)
├── research/               ← research-findings.md  (Phase 01)
├── prds/                   ← final-prd.md  (Phase 02)
├── ux-design.md            ← UX design doc  (Phase 03)
├── architecture-decisions.md ← arch decisions  (Phase 03)
├── epics/                  ← epic-*.md files  (Phase 04)
└── stories/                ← story-*.md Gherkin files  (Phase 04)
```

> Outputs are gitignored by default. Once reviewed, move final docs to `docs/PRDs/` and add to `mkdocs.yml` nav for publication.

---

## Directory Structure

```
tools/bmm/
├── config.yaml                         # BMM configuration (user, paths, Atlassian)
├── README.md                           # This file
├── core/
│   ├── workflow.xml                    # Core workflow execution engine (BMAD OS)
│   ├── agent-manifest.csv             # Agent registry
│   └── workflows/
│       ├── party-mode/                # Multi-agent critique sessions
│       ├── brainstorming/             # Creative ideation sessions
│       └── advanced-elicitation/      # Deep-dive elicitation methods
├── tasks/
│   └── remote-context-discovery.md   # Shared task: context loading
├── output/                            # Generated artefacts (gitignored)
└── workflows/
    ├── pm-execution.yaml              # Full concept-to-story orchestration
    ├── 1-analysis/
    │   ├── create-product-brief/      # Product brief workflow (6 steps)
    │   └── research/                  # Market, domain, and technical research
    ├── 2-plan-workflows/
    │   ├── create-prd/                # PRD creation, validation, and editing
    │   └── create-ux-design/          # UX design workflow (14 steps)
    ├── 3-solutioning/
    │   ├── create-architecture/       # Architecture decision workflow
    │   ├── create-epics-and-stories/  # Epic and story decomposition
    │   └── check-implementation-readiness/ # Pre-dev readiness check
    ├── 4-implementation/
    │   ├── create-story/              # Individual story context prep
    │   ├── sprint-planning/           # Sprint status tracking
    │   ├── sprint-status/             # Sprint status summary
    │   ├── retrospective/             # Post-epic retrospective
    │   └── correct-course/            # Mid-sprint change management
    └── quick-spec/                    # Lightweight spec for small changes
```

---

[Back to tools/](../README.md)
