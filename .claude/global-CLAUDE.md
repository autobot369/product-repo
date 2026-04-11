# Global Claude Code — PM Workspace System Prompt

This file is loaded automatically by Claude Code in **every project**. It bootstraps the BMM (BMAD Method) PM workflow system globally — no per-repo setup needed beyond a thin `tools/bmm/config.yaml`.

---

## Global AI System

Agents, skills, and the BMM workflow engine are installed globally at `~/.claude/`.

```
~/.claude/
├── CLAUDE.md           ← this file (loaded in every repo)
├── agents/             ← 5 role personas, loaded globally
│   ├── pm.md           ← Optimus Prime — pipeline orchestrator
│   ├── analyst.md      ← Bumblebee — market research
│   ├── architect.md    ← Wheeljack — architecture + ADRs
│   ├── ux-designer.md  ← Arcee — UX journey mapping
│   └── sm.md           ← Ironhide — Gherkin stories + Jira
├── skills/             ← 7 slash-command playbooks, loaded globally
│   ├── create-product-brief.md
│   ├── market-research.md
│   ├── create-prd.md
│   ├── ux-journeys.md
│   ├── create-architecture.md
│   ├── confluence-user-stories.md
│   └── user-stories.md
└── bmm/                ← BMM workflow engine (shared, never edited per-repo)
    ├── core/           ← workflow.xml, party-mode, brainstorming
    ├── workflows/      ← pm-execution.yaml + all phase workflows
    ├── data/           ← handoff template, project context template
    ├── tasks/          ← remote-context-discovery, remote-output-push
    └── teams/          ← default-party, team-fullstack
```

---

## Per-Repo Setup (required in any repo you work from)

Each repo needs only a **thin config** to declare its project-specific paths:

```
tools/bmm/
├── config.yaml         ← thin per-repo config (5–6 fields, committed)
└── output/             ← generated artifacts (gitignored)
    ├── briefs/
    ├── research/
    ├── prds/
    ├── stories/
    └── handoff-*.md
```

### Minimal `tools/bmm/config.yaml` template

```yaml
project_name: my-repo
user_skill_level: intermediate   # beginner | intermediate | expert
project_knowledge: "{project-root}/docs"
output_folder: "{project-root}/tools/bmm/output"
user_name: PM
communication_language: English
document_output_language: English
primary_model: claude-sonnet-4-6
```

Agents load this file on activation (step 2 of every agent). If this file is missing, agents will stop and report an error.

---

## Invoke Agents (any repo)

```
# Full pipeline — recommended entry point
Use @~/.claude/agents/pm.md → [RW] Run PM Execution Workflow

# Individual agents
Use @~/.claude/agents/pm.md        — Optimus Prime (PM + orchestrator)
Use @~/.claude/agents/analyst.md   — Bumblebee (market research)
Use @~/.claude/agents/architect.md — Wheeljack (architecture + ADRs)
Use @~/.claude/agents/ux-designer.md — Arcee (UX journeys)
Use @~/.claude/agents/sm.md        — Ironhide (Gherkin stories + Jira)
```

## Invoke Skills (any repo)

```
/create-product-brief   Initiative: [name]  Idea: [description]
/market-research        Topic: [area]
/create-prd             Initiative: [name]  Business Problem: ...
/ux-journeys            PRD: tools/bmm/output/prds/final-prd.md
/create-architecture    PRD: tools/bmm/output/prds/final-prd.md
/confluence-user-stories  Jira project: SQUAD1  Epic: SQUAD1-100
/user-stories           PRD: [url]  Jira project: SQUAD1  Board ID: 7
```

---

## Pipeline Phases

```
Phase 01 — Context Discovery
  Optimus Prime (/create-product-brief) + Bumblebee (/market-research)
  ↓ Gate: Strategic Alignment [party-mode]

Phase 02 — Solutioning Sprint
  Optimus Prime (/create-prd) + Arcee (/ux-journeys inline)
  ↓ Gate: Technical Readiness [party-mode]

Phase 03 — Architecture
  Wheeljack (/create-architecture) → readiness check
  ↓ Gate: Implementation Readiness [auto or party-mode]

Phase 04 — One-Shot Backlog
  Optimus Prime (/confluence-user-stories) → Ironhide (/user-stories + Jira)
  ↓ Post-process: Gherkin validator
```

All outputs land in `{project-root}/tools/bmm/output/` (per-repo, gitignored). Commit selectively to `docs/` once reviewed.

---

## Setting Up a New Repo

1. Create `tools/bmm/config.yaml` with the minimal template above
2. Create `tools/bmm/output/` (will be auto-populated on first run)
3. Add to `.gitignore`:
   ```
   tools/bmm/output/
   ```
4. Invoke any agent or skill — the global engine handles the rest

No other installation required. Agents, skills, and the BMM engine are already available from `~/.claude/`.
