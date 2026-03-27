# Product Management Repository

A structured workspace for product teams — documentation, user journeys, PRDs, specs, experiments, and AI-assisted PM tooling. Built on [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) for publishing and the [BMAD Method](https://github.com/bmad-method/BMAD-METHOD) for AI-assisted product workflows.

---

## Repository Structure

```
├── docs/                  # Published knowledge base (MkDocs)
│   ├── PRDs/              # Product requirement documents
│   ├── specs/             # Technical and functional specifications
│   ├── research/          # UX research, competitive analysis, discovery
│   ├── experiments/       # A/B tests and experiment definitions
│   ├── user-journeys/     # UX flows across the customer funnel
│   └── product-log/       # Historical product decisions
│
├── tools/                 # Internal utilities
│   ├── config.yml         # Shared non-secret configuration for all tools
│   ├── bmm/               # PM workflow engine (concept → PRD → epics → stories)
│   ├── confluence-migration/  # Migrates Confluence spaces into docs/ as Markdown
│   ├── jira-monitor/      # Sprint, release, demand, and pipeline reporting
│   └── pm-workers/        # Claude-powered agents for PRD creation and research
│
├── .claude/               # AI agent personas and skill playbooks
├── tests/                 # Tests for tooling and automation
├── .env.example           # Credential template — copy to .env
└── mkdocs.yml             # Documentation site configuration
```

---

## Prerequisites

| Requirement | Notes |
|-------------|-------|
| Python 3.10+ | Each tool manages its own virtualenv |
| [Claude Code](https://claude.ai/code) | Required for BMM agents and pm-workers skills |
| Atlassian account | Confluence + Jira access with an [API token](https://id.atlassian.com/manage-profile/security/api-tokens) |
| Anthropic API key | For Claude-powered agents and classifier fallback |

---

## Setup

### 1. Credentials

```bash
cp .env.example .env
# Edit .env with your Atlassian email, API token, and Anthropic key
```

### 2. Configuration

Edit `tools/config.yml` — single source of truth for all non-secret settings:

```yaml
atlassian:
  base_url: https://your-org.atlassian.net

jira:
  projects:
    squad1: MYTEAM

confluence:
  spaces:
    - key: PROD
      label: "Product Team"
```

### 3. Documentation site

```bash
python -m venv .venv
source .venv/bin/activate
pip install mkdocs-material mkdocs-awesome-pages-plugin mkdocs-glightbox
mkdocs serve          # http://localhost:8000
mkdocs gh-deploy      # deploy to GitHub Pages
```

### 4. AI agents and skills

Agent personas live in `.claude/agents/` and slash-command skills in `.claude/skills/`. Use with Claude Code directly, or run the full PM workflow via the BMM engine.

---

## Tools

| Tool | What it does | Details |
|------|-------------|---------|
| **BMM** | AI-assisted PM workflows: brief → PRD → epics → stories | [tools/bmm/README.md](tools/bmm/README.md) |
| **Confluence Migration** | Converts Confluence spaces into versioned Markdown in `docs/` | [tools/confluence-migration/](tools/confluence-migration/) |
| **Jira Monitor** | Sprint, release, and demand reporting published to Confluence | [tools/jira-monitor/](tools/jira-monitor/) |
| **PM Workers** | Claude-powered slash commands for PRD creation, research, and story generation | [tools/pm-workers/](tools/pm-workers/) |

---

## Contributing

### Adding product docs

1. **From scratch** — create a file in the appropriate `docs/` subdirectory using this frontmatter:
   ```yaml
   ---
   title: "Feature Name PRD"
   category: prd
   labels: [checkout, q2-2025]
   status: draft
   ---
   ```
2. **From Confluence** — run the confluence-migration pipeline. Synced files are updated on subsequent runs; do not hand-edit them.
3. **From BMM output** — review files in `tools/bmm/output/`, then copy approved artefacts into `docs/PRDs/` or the relevant subdirectory.

### Adding docs sections

When adding a new top-level directory under `docs/`, update the `nav` in `mkdocs.yml` and add an `index.md` to the new directory.

---

## Environment Variables

| Variable | Where used |
|----------|-----------|
| `ATLASSIAN_EMAIL` | confluence-migration, jira-monitor, pm-workers |
| `ATLASSIAN_API_TOKEN` | confluence-migration, jira-monitor, pm-workers |
| `ANTHROPIC_API_KEY` | pm-workers agents, confluence-migration classifier fallback |
