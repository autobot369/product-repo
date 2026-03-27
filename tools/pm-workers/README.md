# PM Workers

Claude-powered agents for PM productivity. Each agent is a Claude Code **skill** — invoke interactively in Claude Code or run programmatically via `run.py`.

All agents connect to Confluence and Jira via the Atlassian MCP server. Configuration is read from `tools/config.yml`. Credentials come from `.env` at repo root.

---

## Setup

### 1. Install dependencies

```bash
cd tools/pm-workers
pip install -r requirements.txt
```

### 2. Credentials

Set in `.env` at repo root (copied from `.env.example`):

```
ANTHROPIC_API_KEY=your-anthropic-key
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
    squad1: MYPROJECT    # default Jira project for story creation

pm_workers:
  read_space:    TEAM    # Confluence space key agents search for context
  publish_space: TEAM    # Confluence space key agents publish PRDs and research to

  prd_parent_page_id:             "123456"   # parent page for new PRDs
  market_research_parent_page_id: "123457"   # parent page for monthly market-research reports

  default_jira_project: MYPROJECT  # Jira project key used when none is specified
  story_label: pm-agent-generated  # label applied to all agent-created Jira issues

  scheduler:
    fire_day:  4          # day of month to run monthly market-research (1–28)
    fire_hour: 9          # hour in 24h format
    fire_min:  0
    timezone:  UTC        # pytz timezone string, e.g. "America/New_York", "Europe/London"
    topic:     "Tier 1 competitor and innovation trends monthly scan"
```

> Page IDs are found in the URL of any Confluence page: `.../pages/PAGE_ID/...`

Leave a page ID as `""` to skip that publish target — the agent will still run and output locally.

---

## Agents

| Agent | Skill | Reads | Writes |
|-------|-------|-------|--------|
| PRD Creator | `/create-prd` | Confluence (context search) | Confluence (new/updated PRD page) |
| User Story Generator | `/user-stories` | Confluence PRD or space search, Jira sprints | Jira (new Story issues, optional sprint assignment) |
| Market Research | `/market-research` | Web + Confluence | Confluence (new research report page) |
| Confluence User Stories | `/confluence-user-stories` | Confluence (full space scan), Jira | Jira (bulk Story issues) |

---

## Invoke via Claude Code (interactive)

```
/create-prd
Initiative: Mobile Checkout Redesign
Business Problem: High cart abandonment at payment step (current: 42%, target: 25%)
User Problem: Users drop off when asked to re-enter payment details
Ideal Solution: One-tap checkout with saved payment methods
Metrics: Cart abandonment rate, checkout conversion rate
```

```
/user-stories
PRD: https://your-org.atlassian.net/wiki/spaces/TEAM/pages/12345
Jira project: SQUAD1
Epic: SQUAD1-42
Board ID: 7
```

```
/market-research
Topic: AI personalisation in retail 2026
Markets: US, UK, AU
Depth: full
```

```
/confluence-user-stories
Space: TEAM
Jira project: SQUAD1
Epic: SQUAD1-100
Filter: checkout
```

---

## Invoke via CLI (programmatic / scheduled)

```bash
cd tools/pm-workers

# PRD Creator
python run.py create-prd \
    --arg "Initiative=Mobile Checkout Redesign" \
    --arg "Business Problem=High cart abandonment at payment step" \
    --arg "User Problem=Users drop off when asked to re-enter payment details" \
    --arg "Ideal Solution=One-tap checkout with saved payment methods" \
    --arg "Metrics=Cart abandonment rate, checkout conversion rate"

# User Story Generator
python run.py user-stories \
    --arg "PRD=https://your-org.atlassian.net/wiki/spaces/TEAM/pages/12345" \
    --arg "Jira project=SQUAD1" \
    --arg "Epic=SQUAD1-42" \
    --arg "Board ID=7"

# Market Research
python run.py market-research \
    --arg "Topic=AI personalisation in retail 2026" \
    --arg "Markets=US,UK,AU" \
    --arg "Depth=full"

# Confluence User Stories
python run.py confluence-user-stories \
    --arg "Space=TEAM" \
    --arg "Jira project=SQUAD1" \
    --arg "Epic=SQUAD1-100"
```

---

## Monthly scheduler (market-research)

Fires `/market-research` automatically on the configured schedule (default: 4th of each month at 09:00 UTC). Schedule, timezone, and research topic are all set in `tools/config.yml` under `pm_workers.scheduler`. Reports are published to Confluence under `pm_workers.market_research_parent_page_id`.

```bash
# Start in background (survives terminal close)
nohup python scheduler.py > scheduler.log 2>&1 &

# Test immediately
python scheduler.py --run-now

# Stop
kill $(cat scheduler.pid)
```

---

## End-to-end workflow

```
1. /market-research
   → competitive landscape or research report in Confluence
   ↓
2. Identify a gap or opportunity
   ↓
3. /create-prd
   → full PRD in Confluence under your space → Feature Grooming
   ↓
4. Review and refine (add Figma, answer Open Questions)
   ↓
5. /user-stories  (PRD URL + Jira project + Epic + Board ID)
   → stories created in Jira, assigned to next sprint
   ↓
6. Grooming session — stories already in Jira, team estimates
```

For a legacy space with undocumented features, run `/confluence-user-stories` alongside step 5.

**Typical time saved:** ~2–3 hours per initiative (PRD + story creation) + 1–2 hours of competitive research per quarter.

---

## Configuration

| Setting | Location | Key |
|---------|----------|-----|
| Confluence space to read context from | `tools/config.yml` | `pm_workers.read_space` |
| Confluence space to publish PRDs/research to | `tools/config.yml` | `pm_workers.publish_space` |
| Parent page for new PRDs | `tools/config.yml` | `pm_workers.prd_parent_page_id` |
| Monthly market-research parent page | `tools/config.yml` | `pm_workers.market_research_parent_page_id` |
| Default Jira project for story creation | `tools/config.yml` | `pm_workers.default_jira_project` |
| Story label for generated tickets | `tools/config.yml` | `pm_workers.story_label` |
| Monthly market-research scheduler day/time | `tools/config.yml` | `pm_workers.scheduler.*` |
| Atlassian base URL, project keys | `tools/config.yml` | `atlassian.*`, `jira.projects` |
| `ANTHROPIC_API_KEY`, `ATLASSIAN_EMAIL`, `ATLASSIAN_API_TOKEN` | `.env` (repo root) | — |
| Agent skill prompts | `.claude/skills/*.md` | — |

To point agents at a different Confluence space (e.g. for a new team or business unit), update `read_space` and `publish_space` in `tools/config.yml` — no code changes required.

---

[Back to tools/](../README.md)
