# Claude.md — Product Repo (project-scoped context)

> **AI System:** Agents, skills, and the BMM engine are installed globally at `~/.claude/` and load automatically in every repo.
> See `~/.claude/CLAUDE.md` for full system documentation, setup instructions, and pipeline reference.

This file adds product-repo–specific context on top of the global system.

---

## Repository Structure

```
.claude/
└── claude.md           ← this file (project-specific context only)

docs/                   ← DEFAULT KNOWLEDGE BASE (MkDocs source)
├── index.md
├── PRDs/               ← Product Requirement Documents
├── research/           ← Research documents
├── user-journeys/      ← UX flows by funnel stage
│   ├── Front_Funnel/
│   ├── Mid_Funnel/
│   ├── Bottom_Funnel/
│   └── Loyalty/
├── product-log/        ← Year-grouped PRD/research index
└── specs/              ← Technical specifications

tools/
├── bmm/
│   ├── config.yaml     ← Per-repo BMM config (committed) — edit for project settings
│   └── output/         ← Generated artifacts (gitignored — commit selectively to docs/)
│       ├── briefs/
│       ├── research/
│       ├── prds/
│       ├── stories/
│       └── handoff-*.md
├── confluence-migration/
├── jira-monitor/
└── pm-workers/

tests/
README.md
mkdocs.yml
```

---

## MkDocs Commands

```bash
source .venv/bin/activate
mkdocs serve      # local dev with live reload
mkdocs build      # build static site
mkdocs gh-deploy  # deploy to GitHub Pages
```

---

## Content Architecture

- `docs/user-journeys/` — Funnel-stage docs (Front → Mid → Bottom → Loyalty)
- `docs/PRDs/` — Product Requirement Documents per feature/initiative
- `docs/specs/` — Technical and functional specifications
- Navigation driven by `mkdocs.yml` — add new sections there when adding top-level directories
- The `tags` plugin enables cross-linking content across sections

---

## Adding Content

- **PRDs**: Place in `docs/PRDs/` and add to `mkdocs.yml` nav
- **User journeys**: Place in `docs/user-journeys/<Funnel>/`
- **Specs**: Place in `docs/specs/`
- **Scripts / utilities**: Place in `tools/`
- **Tests**: Place in `tests/`

---

## Invoking the AI System (from this repo)

Agents and skills are globally available — no `@product-repo/` prefix needed.

```
# Full pipeline (recommended)
Use @~/.claude/agents/pm.md → [RW] Run PM Execution Workflow

# Individual agents
Use @~/.claude/agents/pm.md
Use @~/.claude/agents/analyst.md
Use @~/.claude/agents/architect.md
Use @~/.claude/agents/ux-designer.md
Use @~/.claude/agents/sm.md

# Skills
/create-product-brief   Initiative: [name]
/market-research        Topic: [area]
/create-prd             Initiative: [name]
/ux-journeys            PRD: tools/bmm/output/prds/final-prd.md
/create-architecture    PRD: tools/bmm/output/prds/final-prd.md
/confluence-user-stories  Jira project: SQUAD1
/user-stories           Jira project: SQUAD1  Board ID: 7
```

BMM config for this repo: [tools/bmm/config.yaml](../tools/bmm/config.yaml)
