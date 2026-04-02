---
description: Runs targeted web searches combined with Confluence context to produce a structured market research report, then publishes it to Confluence. Use for deep-dive research on a specific topic before writing a PRD or to justify a roadmap decision. Invoke with a topic; markets, competitors, and depth are optional.
bmm_phase: "01_Accelerated_Context_Discovery"
bmm_step: "market_research"
bmm_agent: analyst
bmm_runs: standalone_or_orchestrated
output_file: "tools/bmm/output/research/research-findings.md"
output_contract:
  required_sections:
    - Executive Summary
    - Competitive Landscape
    - Market Lens
    - Opportunity Assessment
    - Recommendations
  min_recommendations: 3
handoff_writes:
  - key: research_complete
    value: true
  - key: research_output
    value: "tools/bmm/output/research/research-findings.md"
dependencies:
  - Confluence: search space, read pages, create page, add labels
  - WebSearch: targeted competitor and market queries
---

# /market-research — Market Research

## Invoke

```
/market-research
Topic: [research question or market area]
Markets: US, UK, AU         (optional — specify relevant markets)
Competitors: Acme, Rival    (optional — defaults to primary competitors)
Depth: full                 (optional — "summary" for 1-page overview, "full" for detailed report)
```

## 1 — Gather Confluence context

Search the Confluence space for existing research, prior analyses, and relevant PRDs related to the topic — read 3–5 pages to understand what is already known internally, identify gaps external research should fill, and source correct team terminology.

## 2 — Run web research

Execute targeted searches for each competitor and market specified:

| Query pattern | Purpose |
|---|---|
| `[Topic] [Competitor] [Year]` | Competitor activity and announcements |
| `[Topic] [Market] consumer behaviour [Year]` | Regional adoption and behaviour signals |
| `[Topic] technology trends [Year]` | Emerging and declining patterns |
| `[Competitor] [Topic] case study OR announcement` | Specific product moves |

For each hit: fetch the page if accessible, note source, date, and relevance — flag any finding that directly impacts the current roadmap.

## 3 — Build research report

Compile findings into a structured report:

| Section | Contents |
|---------|----------|
| Executive Summary | 3–5 bullet findings, top recommendation |
| Competitive Landscape | Per-competitor summary: what they offer, what's new, gaps vs. your product |
| Market Lens | Market-by-market relevance — adoption rates, consumer behaviour, regulatory context |
| Technology & Trend Analysis | What's emerging, what's mainstream, what's declining |
| Opportunity Assessment | Where the product is ahead, at parity, or behind; opportunity size where data exists |
| Recommendations | 3–5 actionable items ranked by urgency, each mapped to a specific product area |

| Depth param | Output |
|---|---|
| `summary` | Executive Summary + Recommendations only |
| `full` (default) | All sections |

## 4 — Publish to Confluence

Create a new page in the configured space under the Research parent — title format: `[Topic] — Market Research [YYYY-MM]` — add labels: `research`, `market-research`, `pm-agent-generated` — output the page URL.

## Output

Confluence research report page containing all sections appropriate to the requested depth.

**Side effects:** Creates a Confluence page with labels `research`, `market-research`, `pm-agent-generated`.

## Guidelines

- Do not hallucinate competitor features — if no strong signal exists, write "No material findings for [Competitor] in this area."
- Every recommendation must be concrete enough to become a PRD brief or backlog item.
- If a finding maps to an existing PRD in Confluence, reference it by page link.
- Flag any finding older than 6 months as potentially outdated.
- Produce `depth: summary` as Executive Summary + Recommendations only — never expand without explicit request.
