---
description: Ad-hoc competitive intelligence scanner. Runs a targeted web scan of competitor activity, news, and signals, then publishes a log entry to Confluence. For deep-dive structured research, use /market-research instead.
dependencies:
  - Confluence: read pages, create/update page, add labels
  - WebSearch: competitor news, hiring signals, product announcements
---

# /omni-monitor — Omni-Channel Competitive Monitor

> For structured research reports, use [/market-research](.claude/skills/market-research.md).
> This skill is for ad-hoc signal capture — quick scans, hiring spikes, launch alerts.

## Invoke

```
/omni-monitor
[Free-form request describing what to scan]
```

Examples:
```
/omni-monitor
run a parallel scan of Tier 1 competitors and summarise hiring spikes in AI over the last 30 days
```
```
/omni-monitor
check for loyalty or rewards product launches from [Competitor A], [Competitor B], and [Competitor C] in Q1 2026
```

## How it works

1. **Parse** the request — extract competitors, signal types (launches, hiring, pricing, press), and time window (default: last 30 days)
2. **Scan** — run parallel web searches per competitor × signal type; fetch accessible pages; extract headline, date, source URL, signal type, and one-sentence summary
3. **Compile** — organise into a scan log table grouped by competitor; flag any finding dated within the last 7 days as **Recent**; write "No material findings." where nothing exists
4. **Publish** — append a dated entry to the omni-monitor log page at `pm_workers.omni_log_page_id`; if not configured, create `Competitive Intelligence Log [YYYY-MM]` under the publish space; add labels `competitive-intel`, `omni-monitor`, `pm-agent-generated`; output the page URL

## Guidelines

- Report only findings backed by a source URL — do not infer or extrapolate
- If a source is paywalled, note "Source inaccessible" and skip
- Flag findings older than 30 days as potentially stale
- One row per finding, one sentence per summary
- For structured analysis of findings, hand off to `/market-research`
