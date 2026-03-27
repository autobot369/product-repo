# Product Management Repository

A structured workspace for product teams — documentation, user journeys, PRDs, specs, experiments, and AI-assisted PM tooling. Built on [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) for publishing and the [BMAD Method](https://github.com/bmad-method/BMAD-METHOD) for AI-assisted product workflows.

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

Edit `tools/config.yml` — this is the single source of truth for all non-secret settings:

```yaml
atlassian:
  base_url: https://your-org.atlassian.net   # your Atlassian Cloud URL

jira:
  projects:
    squad1: MYTEAM                           # your Jira project key(s)

confluence:
  spaces:
    - key: PROD                              # Confluence space key(s) to migrate
      label: "Product Team"
```

Confluence page IDs (for jira-monitor and pm-workers publish targets) can be found in the URL of any Confluence page: `…/pages/PAGE_ID/…`.

### 3. Documentation site

```bash
python -m venv .venv
source .venv/bin/activate
pip install mkdocs-material mkdocs-awesome-pages-plugin mkdocs-glightbox
mkdocs serve
```

The site will be available at `http://localhost:8000`. Deployments to GitHub Pages happen automatically on push to `main` (configure via GitHub Actions if not already set up).

### 4. AI agents and skills

This repo is designed to be used with Claude Code. Agent personas and slash-command skills live in `.claude/agents/` and `.claude/skills/`. These are not included in this template — add your own, or see the [BMM README](tools/bmm/README.md) for the expected agent structure.

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
├── tests/                 # Tests for tooling and automation
├── .env.example           # Credential template — copy to .env
├── .env                   # Your credentials (gitignored)
└── mkdocs.yml             # Documentation site configuration
```

---

## Tools

### BMM — PM Workflow Engine

Runs structured AI-assisted workflows: market research → product brief → PRD → epics → user stories → sprint planning.

```bash
# All output goes to tools/bmm/output/ (gitignored)
# Review output, then commit selectively to docs/
```

Invoke via Claude Code using the `bmm` agent personas. See [tools/bmm/README.md](tools/bmm/README.md) for the full workflow reference.

**Key config**: `tools/bmm/config.yaml`
- `user_name` — personalise the PM name the agents address
- `prd_intake_mode` — `strategic-core` (single dense prompt) or `step-by-step` (multi-turn facilitation)

---

### Confluence Migration

Reads one or more Confluence spaces and converts pages into clean Markdown files, categorised as PRDs, specs, research, or A/B tests.

```bash
cd tools/confluence-migration
pip install -r requirements.txt

# Copy and edit the config template
cp config.example.yml config.yml
# Edit config.yml: add your Confluence space keys and classifier rules

# Dry run (fetch + classify, no writes)
python -m confluence_migration --config config.yml --dry-run

# Full run with stage gates
python -m confluence_migration --config config.yml

# Resume from a specific stage (uses cached output)
python -m confluence_migration --config config.yml --from-stage classify
python -m confluence_migration --config config.yml --from-stage convert
```

Stage gates pause at each step so you can review and edit before proceeding. The tool will not overwrite docs that don't have a `confluence_id` in their frontmatter — handcrafted files are protected.

---

### PM Workers

Claude-powered agents for everyday PM tasks. Run interactively via Claude Code slash commands, or programmatically via the CLI.

```bash
cd tools/pm-workers
pip install -r requirements.txt
```

| Skill | What it does |
|-------|-------------|
| `/create-prd` | Drafts a full PRD and publishes to Confluence |
| `/user-stories` | Generates Jira stories from a PRD or Confluence page |
| `/omni-monitor` | Scans competitors and summarises signals |
| `/market-research` | Produces a structured research report |
| `/confluence-user-stories` | Bulk-creates Jira stories from an entire Confluence space |

**Interactive (Claude Code):**
```
/create-prd
Initiative: Loyalty Scan & Earn
Business Problem: Low in-store scan adoption
Ideal Solution: In-app prompt with scan confirmation flow
Metrics: Scan rate, loyalty attach rate
```

**CLI / scheduled:**
```bash
python run.py create-prd \
    --arg "Initiative=Loyalty Scan & Earn" \
    --arg "Metrics=Scan rate, attach rate"

# Monthly competitive monitor (fires on day/time set in tools/config.yml)
python scheduler.py
```

---

### Jira Monitor

Automated reporting for sprint reviews, release tracking, demand pipeline, and feature pipeline. Reads from Jira and publishes reports to Confluence.

```bash
cd tools/jira-monitor
pip install -r requirements.txt
python -m jira_monitor --config ../config.yml
```

Configure publish targets (Confluence page IDs) under `jira_monitor` in `tools/config.yml`.

---

## Contributing

### Adding product docs

1. **From scratch** — create a file in the appropriate `docs/` subdirectory. Use the frontmatter format:
   ```yaml
   ---
   title: "Feature Name PRD"
   category: prd
   labels: [checkout, q2-2025]
   status: draft
   ---
   ```

2. **From Confluence** — run the confluence-migration pipeline. Synced files will be updated on subsequent runs; do not hand-edit them.

3. **From BMM output** — review files in `tools/bmm/output/`, then copy approved artefacts into `docs/PRDs/` or the relevant subdirectory.

### Adding docs sections

When adding a new top-level section to `docs/`, update the `nav` in `mkdocs.yml` to publish it.

---

## Environment Variables Reference

| Variable | Where used |
|----------|-----------|
| `ATLASSIAN_EMAIL` | confluence-migration, jira-monitor, pm-workers |
| `ATLASSIAN_API_TOKEN` | confluence-migration, jira-monitor, pm-workers |
| `ANTHROPIC_API_KEY` | pm-workers agents, confluence-migration classifier fallback |

All three must be set in `.env` for full functionality. The confluence-migration tool can run in fetch/classify mode without `ANTHROPIC_API_KEY` — it's only used as a classifier fallback for ambiguous pages.
