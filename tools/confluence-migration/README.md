# confluence-migration

Reads one or more Confluence spaces and categorises pages into the repository as Markdown files, ready for AI agents to consume.

**Output targets:**
- `docs/PRDs/` — Product Requirement Documents
- `experiments/` — A/B tests and experiment definitions
- `docs/specs/` — Technical and feature specifications

---

## How it works

```
fetch → [GATE] → classify → [GATE] → convert → [GATE*] → write
```

Each stage writes its output to disk. Stage gates pause and ask you to review before proceeding. You can edit the intermediate files (page list, classification manifest, Markdown previews) before each gate.

`*` Gate 3 is off by default — enable in `config.yml` if you want to review Markdown before it lands in `docs/`.

---

## Setup

```bash
cd tools/confluence-migration
pip install -r requirements.txt
cp config.example.yml config.yml
# Edit config.yml with your Confluence base URL and space keys
```

Set credentials in your environment (never in config.yml):

```bash
export ATLASSIAN_EMAIL=you@yourcompany.com
export ATLASSIAN_API_TOKEN=your-token

# Optional: enables Claude fallback classifier for ambiguous pages
export ANTHROPIC_API_KEY=your-key
```

---

## Run

```bash
# Full pipeline with stage gates
python -m confluence_migration --config config.yml

# Dry run — fetch and classify but don't write to docs/
python -m confluence_migration --config config.yml --dry-run

# Resume from a specific stage (uses cached output)
python -m confluence_migration --config config.yml --from-stage classify
python -m confluence_migration --config config.yml --from-stage convert
python -m confluence_migration --config config.yml --from-stage write
```

---

## Stage gate files

| Stage | Output file | What to review |
|-------|-------------|----------------|
| After fetch | `cache/pages.json` | Remove pages you don't want migrated |
| After classify | `output/classification.yml` | Correct any wrong categories (`prd` / `abtest` / `spec` / `skip`) |
| After convert *(optional)* | `output/preview/` | Check Markdown formatting and front matter tags |

---

## Classification logic

Pages are classified in priority order:

1. **Confluence labels** — mapped via `label_map` in config
2. **Title heuristics** — keyword matching via `heuristics` in config
3. **Claude API** — falls back to `claude-haiku` for ambiguous pages (requires `ANTHROPIC_API_KEY`)
4. **`unknown`** — written to `output/unclassified/` for manual review

---

## Safety

- The writer **will not overwrite** existing files that don't have a `confluence_id` in their front matter — handcrafted docs are protected.
- Re-running the tool on already-migrated files is safe; it will update them.
- `--dry-run` skips the write stage entirely.

---

## Output front matter

Every migrated file gets:

```yaml
---
title: "Search Re-ranking PRD"
confluence_id: "123456"
confluence_url: https://yourcompany.atlassian.net/wiki/spaces/SEA/pages/123456
category: prd
labels: [search, front-funnel, q2-2025]
space_key: SEA
last_updated: 2026-03-24
---
```

Agents can filter by `category` and `labels` to find relevant documents.

---

[Back to tools/](../README.md)
