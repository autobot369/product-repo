---
name: 'remote-context-discovery'
description: 'Search Confluence and Jira for related context before starting any BMM workflow. Injected by all BMM init steps.'
---

# Task: Remote Context Discovery

## PURPOSE

Enrich the workflow with live Confluence and Jira context before beginning collaborative discovery. This task runs during workflow initialization after local file discovery, and before the user proceeds to step 2.

## MANDATORY EXECUTION RULES

- 📖 Read this entire task file before taking any action
- 🛑 NEVER block workflow progression — remote discovery is enrichment, not a gate
- ✅ Always report findings to user and include in `inputDocuments` frontmatter
- 🔄 If MCP tools are unavailable, skip gracefully and note it in the report
- 🚫 FORBIDDEN to load more than 5 Confluence pages total (keep context lean)

## CONFIGURATION (resolved from config.yaml)

- `{confluence_search_space}` — space to search (default: ISD)
- `{confluence_feature_grooming_page_id}` — parent page for Feature Grooming
- `{jira_project}` — Jira project key for issue lookup

---

## EXECUTION SEQUENCE

### 1. Derive Search Terms

From the current workflow context (project name, topic, user messages so far), derive 2–3 search terms that represent the product area being worked on.

Example: For a product brief about "Skincredible AI Routine", use:
- `"Skincredible"`, `"AI Routine"`, `"POTION recommendations"`

### 2. Search Confluence

Use the Atlassian MCP tool to search the `{confluence_search_space}` space:

```
Search query: [derived search terms]
Space filter: {confluence_search_space}
Limit: 10 results
```

From results, identify the **3–5 most relevant pages** based on:
- Title relevance to current workflow topic
- Pages under Feature Grooming (ancestor: `{confluence_feature_grooming_page_id}`)
- Recent/active documents (higher version numbers preferred)

### 3. Fetch Relevant Pages

For each selected page, fetch the full content using the Confluence MCP tool (convert to markdown). Load ALL fetched pages completely — no offset/limit.

Track each successfully fetched page in a list for reporting.

### 4. Search Jira for Related Issues (Optional)

If the workflow is a PRD, Architecture, or Epic/Story workflow, also search Jira:

```
Query: project = {jira_project} AND text ~ "[search term]" ORDER BY updated DESC
Limit: 5 issues
```

For each result, note: issue key, summary, status, and any linked epic.

This provides awareness of existing in-flight work to avoid duplication and surface dependencies.

### 5. Report Findings to User

Present a concise summary:

```
**🔗 Remote Context Loaded from Confluence:**

- [Page Title 1](URL) — [1-line summary of what it contains]
- [Page Title 2](URL) — [1-line summary]
- [Page Title 3](URL) — [1-line summary]

**📋 Related Jira Issues Found:** [if applicable]
- [PROJ-123] [Summary] — [Status]
- [PROJ-456] [Summary] — [Status]

These will inform the workflow. You can ask me to load additional pages or Jira issues at any time.
```

If nothing relevant found:

```
**🔗 Remote Context:** No highly relevant Confluence pages found in {confluence_search_space}. Proceeding with local documents only.
```

### 6. Update Frontmatter

Add all fetched Confluence pages and Jira issues to the output document frontmatter:

```yaml
inputDocuments:
  - type: confluence
    title: "[Page Title]"
    url: "[Confluence URL]"
    page_id: "[page ID]"
  - type: jira
    key: "[PROJ-123]"
    summary: "[Issue Summary]"
    status: "[Status]"
```

---

## FAILURE HANDLING

- **MCP unavailable**: Log "Atlassian MCP not available — skipping remote context discovery" and continue
- **No results**: Log "No relevant pages found" and continue
- **Fetch error on individual page**: Skip that page, continue with others
- **Never block the workflow** — this is enrichment only

---

## SUCCESS METRICS

✅ Confluence searched with relevant terms derived from workflow context
✅ 3–5 most relevant pages identified and fetched completely
✅ Jira issues searched when workflow type warrants it
✅ Findings reported to user clearly with page titles and summaries
✅ All remote documents added to frontmatter `inputDocuments`
✅ Workflow continues normally after this task completes
