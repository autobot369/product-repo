# Tools

Internal utilities for the product team.

Credentials are never stored in config — load them from `.env` at repo root (`ATLASSIAN_EMAIL`, `ATLASSIAN_API_TOKEN`, `ANTHROPIC_API_KEY`). Non-secret configuration lives in `tools/config.yml`.

---

## Tools

| Tool | What it does |
|------|-------------|
| [bmm/](bmm/README.md) | PM workflow engine — runs concept → research → PRD → epics → stories via AI agents |
| [confluence-migration/](confluence-migration/README.md) | Migrates Confluence spaces into `docs/` as clean Markdown |
| [jira-monitor/](jira-monitor/) | Automated sprint, release, demand, and feature pipeline reporting |
| [pm-workers/](pm-workers/README.md) | Claude-powered PM agents for PRD creation, story generation, and market research |
| [agent-persona-skill-builder/](agent-persona-skill-builder/README.md) | Interactive CLI to generate token-optimized `.claude/agents/`, `.claude/personas/`, and `.claude/skills/` files |

---

## Shared Config

`tools/config.yml` is the single source of truth for non-secret configuration:

| Key | What it controls |
|-----|-----------------|
| `atlassian.base_url` | Atlassian Cloud instance URL |
| `output.*` | Canonical doc directory paths |
| `jira.projects` | Project key map (isd, auto, oip, mobile, qa) |
| `confluence.spaces` | Spaces used by confluence-migration |
| `confluence.pages` | Well-known Confluence page IDs |
| `confluence_migration.*` | Cache dir, stage gate behaviour |
| `jira_monitor.*` | Stale epic threshold, Confluence publish targets |
| `pm_workers.*` | Read/publish spaces, parent page IDs, scheduler config |

---

[Back to repo root](../README.md)
