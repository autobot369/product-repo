# jira-monitor

Automated sprint, release, demand, and feature pipeline reporting. Reads from Jira, compiles Markdown reports, and publishes them to Confluence.

---

## Setup

### 1. Install dependencies

```bash
cd tools/jira-monitor
pip install -r requirements.txt
```

### 2. Credentials

Set in `.env` at repo root (copied from `.env.example`):

```
ATLASSIAN_EMAIL=you@yourorg.com
ATLASSIAN_API_TOKEN=your-api-token
```

### 3. Configure `tools/config.yml`

All settings live in the global `tools/config.yml`. Update the following before running:

```yaml
atlassian:
  base_url: https://your-org.atlassian.net   # your Atlassian Cloud URL

jira:
  projects:
    squad1: MYPROJECT    # add one entry per Jira project you want reported on
    squad2: MYPROJECT2   # all reporters run against every project listed here

jira_monitor:
  stale_epic_days: 60    # epics with no update older than this are flagged stale

  confluence:
    sprint_reviews_parent:   "123456"   # parent page ID — sprint reviews are created as children
    demand_review_page_id:   "123457"   # page to prepend demand review digests to
    release_tracker_page_id: "123458"   # page to prepend release tracker reports to
    pipeline_page_id:        "123459"   # page to prepend feature pipeline reports to
```

> Page IDs are found in the URL of any Confluence page: `.../pages/PAGE_ID/...`

Leave a page ID as `""` to skip publishing that workstream.

---

## Run

```bash
cd tools/jira-monitor

# All 4 workstreams (parallel)
python -m jira_monitor

# Single workstream
python -m jira_monitor --mode sprint
python -m jira_monitor --mode release
python -m jira_monitor --mode demand
python -m jira_monitor --mode pipeline

# Generate reports without publishing to Confluence
python -m jira_monitor --dry-run

# Skip the confirmation gate before publishing
python -m jira_monitor --no-gate
```

Reports are always written to `output/<mode>-<date>.md` regardless of `--dry-run`.

---

## Workstreams

| Mode | What it reports | Confluence target |
|------|----------------|-------------------|
| `sprint` | Active sprint stories by status, risk flags, demo agenda | Child page under `sprint_reviews_parent` |
| `release` | Unreleased and recently released versions, open blockers | `release_tracker_page_id` |
| `demand` | Epics in backlog/discovery — stale, unassigned, active | `demand_review_page_id` |
| `pipeline` | Epic completion %, blocked stories, research signal cross-reference | `pipeline_page_id` |

---

[Back to tools/](../README.md)
