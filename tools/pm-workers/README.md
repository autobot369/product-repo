# PM Workers

Claude-powered agents for PM productivity. Each agent is a Claude Code **skill** — invoke interactively in Claude Code or run programmatically via `run.py`.

All agents connect to Confluence and Jira via the Atlassian MCP server. Configuration is read from `tools/config.yml`. Credentials come from `.env` at repo root.

---

## Agents

| Agent | Skill | Reads | Writes |
|-------|-------|-------|--------|
| PRD Creator | `/create-prd` | Confluence (context search) | Confluence (new/updated PRD page) |
| User Story Generator | `/user-stories` | Confluence PRD or space search, Jira sprints | Jira (new Story issues, optional sprint assignment) |
| Omni-Channel Monitor | `/omni-monitor` | Web (competitors, news, LinkedIn) | Confluence (log or monthly report page) |
| Market Research | `/market-research` | Web + Confluence | Confluence (new research report page) |
| Confluence User Stories | `/confluence-user-stories` | Confluence (full space scan), Jira | Jira (bulk Story issues) |

---

## Invoke via Claude Code (interactive)

```
/create-prd
Initiative: Loyalty Scan & Earn
Business Problem: Low in-store scan adoption (current: 18%, target: 35%)
User Problem: Associates don't prompt members to scan at POS
Ideal Solution: In-app prompt with scan confirmation flow
Metrics: Scan rate, loyalty attach rate
```

```
/user-stories
PRD: https://your-org.atlassian.net/wiki/spaces/TEAM/pages/12345
Jira project: SQUAD1
Epic: SQUAD1-42
Board ID: 7
```

```
/omni-monitor
run a parallel scan of Tier 1 competitors and summarise hiring spikes in AI over the last 30 days
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
Filter: loyalty
```

---

## Invoke via CLI (programmatic / scheduled)

```bash
cd tools/pm-workers

# PRD Creator
python run.py create-prd \
    --arg "Initiative=Loyalty Scan & Earn" \
    --arg "Business Problem=Low in-store scan adoption" \
    --arg "User Problem=Associates don't prompt members to scan" \
    --arg "Ideal Solution=In-app prompt at POS" \
    --arg "Metrics=Scan rate, loyalty attach rate"

# User Story Generator
python run.py user-stories \
    --arg "PRD=https://your-org.atlassian.net/wiki/spaces/TEAM/pages/12345" \
    --arg "Jira project=SQUAD1" \
    --arg "Epic=SQUAD1-42" \
    --arg "Board ID=7"

# Omni-Monitor
python run.py omni-monitor \
    --arg "Request=run a full parallel scan of Tier 1 competitors"

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

## Monthly scheduler (omni-monitor)

Fires the omni-monitor automatically on the **4th of every month at 09:00**:

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
1. /omni-monitor or /market-research
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
| Omni-monitor log page | `tools/config.yml` | `pm_workers.omni_log_page_id` |
| Omni-monitor monthly report page | `tools/config.yml` | `pm_workers.omni_monthly_page_id` |
| Default Jira project for story creation | `tools/config.yml` | `pm_workers.default_jira_project` |
| Story label for generated tickets | `tools/config.yml` | `pm_workers.story_label` |
| Monthly scheduler day/time | `tools/config.yml` | `pm_workers.scheduler.*` |
| Atlassian base URL, project keys | `tools/config.yml` | `atlassian.*`, `jira.projects` |
| `ANTHROPIC_API_KEY`, `ATLASSIAN_EMAIL`, `ATLASSIAN_API_TOKEN` | `.env` (repo root) | — |
| Agent skill prompts | `.claude/skills/*.md` | — |

To point agents at a different Confluence space (e.g. for a new team or business unit), update `read_space` and `publish_space` in `tools/config.yml` — no code changes required.

---

[Back to tools/](../README.md)
