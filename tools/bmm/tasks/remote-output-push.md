---
name: 'remote-output-push'
description: 'Publish completed BMM artifacts to Confluence and optionally create Jira issues. Injected by all BMM complete steps.'
---

# Task: Remote Output Push

## PURPOSE

After a BMM workflow completes, publish the output document to Confluence and optionally create Jira epics/stories. This task runs as part of the workflow completion step.

## MANDATORY EXECUTION RULES

- 📖 Read this entire task file before taking any action
- 🤝 ALWAYS ask the user before publishing — never auto-publish
- ✅ Check if a page with the same title already exists before creating a new one (update, don't duplicate)
- 🔄 If MCP tools are unavailable, provide the document content for manual copy-paste
- 🚫 Publishing is OPTIONAL — user can skip with [S] Skip

## CONFIGURATION (resolved from config.yaml)

- `{confluence_publish_space}` — target space (default: ISD)
- `{confluence_feature_grooming_page_id}` — parent page ID for Feature Grooming
- `{confluence_prd_labels}` — labels for PRD pages (default: `prd,bmad-generated`)
- `{confluence_brief_labels}` — labels for brief pages (default: `product-brief,bmad-generated`)
- `{jira_project}` — Jira project key
- `{jira_story_label}` — label to apply to generated stories (default: `bmad-generated`)

---

## EXECUTION SEQUENCE

### 1. Present Publishing Menu

Before doing anything, present the user with options:

```
🎉 Your [document type] is complete! Would you like to publish it?

**[P] Publish to Confluence**
  → Creates/updates a page under Feature Grooming in the ISD space
  → Adds labels: {appropriate_labels}

**[J] Create Jira Issues** *(PRD and Epic workflows only)*
  → Generates Jira stories/epics from the completed document
  → Labels all issues: {jira_story_label}

**[B] Both** — Publish to Confluence AND create Jira issues

**[S] Skip** — Save locally only (you can publish manually later)
```

Wait for user selection before proceeding.

---

### 2A. If [P] or [B] — Publish to Confluence

#### Step A: Check for Existing Page

Search Confluence for an existing page with the same or similar title under the Feature Grooming parent:

```
Search: title ~ "[document title]" AND ancestor = "{confluence_feature_grooming_page_id}"
Space: {confluence_publish_space}
```

#### Step B: Create or Update Page

**If page exists:**
- Fetch the existing page to confirm it's the right one
- Update the page with the new content (preserve version history)
- Inform user: "Updated existing page: [Title] — [URL]"

**If no page exists:**
- Create a new child page under `{confluence_feature_grooming_page_id}`
- Title format:
  - Product Brief: `[Project Name]: Product Brief`
  - PRD: `[Feature Name]: PRD`
  - Architecture: `[Feature Name]: Architecture`
  - UX Design: `[Feature Name]: UX Design`
- Content: Full document in markdown format
- Inform user: "Created new page: [Title] — [URL]"

#### Step C: Add Labels

Add appropriate labels to the page:
- Product Brief → `{confluence_brief_labels}`
- PRD → `{confluence_prd_labels}`
- Architecture → `architecture,bmad-generated`
- UX Design → `ux-design,bmad-generated`
- Research → `research,bmad-generated`

#### Step D: Report Result

```
✅ **Published to Confluence:**
   [Page Title](URL)
   Parent: Feature Grooming > ISD
   Labels: [labels applied]
   Action: [Created / Updated]
```

---

### 2B. If [J] or [B] — Create Jira Issues *(PRD/Epic workflows only)*

#### Step A: Extract Stories/Epics from Document

Parse the completed PRD or Epic document for:
- Epic titles (from `## Epic` or `### Epic` headings)
- User stories (from "As a [persona]..." patterns or story tables)
- Acceptance criteria (from bullet lists under stories)
- Dependencies noted in Open Questions section

#### Step B: Confirm with User

Present the extracted list before creating:

```
**Jira Issues to Create (Project: {jira_project}):**

Epic: [Epic Title]
  Story 1: [Summary]
  Story 2: [Summary]
  Story 3: [Summary]

Epic: [Epic Title 2]
  Story 4: [Summary]

Shall I create these? [Y] Yes / [E] Edit list / [N] No
```

#### Step C: Create Issues

Create each issue using the Jira MCP tool:

**For Epics:**
```
issuetype: Epic
project: {jira_project}
summary: [Epic Title]
description: [Epic description from document]
labels: [{jira_story_label}]
```

**For Stories:**
```
issuetype: Story
project: {jira_project}
summary: [Story title, max 10 words]
description: |
  As a [persona], I want to [action] so that [benefit].

  **Acceptance Criteria:**
  - [ ] [criterion]
  - [ ] [criterion]

  **Notes:**
  - Confluence ref: [URL of published page]
labels: [{jira_story_label}]
epic: [parent epic key]
```

Create stories one by one. If creation fails for one, note it and continue with the rest.

#### Step D: Report Result

```
✅ **Jira Issues Created (Project: {jira_project}):**

| Key | Summary | Type | Status |
|-----|---------|------|--------|
| ISD-XXXX | [Summary] | Epic | Open |
| ISD-XXXX | [Summary] | Story | Open |
| ISD-XXXX | [Summary] | Story | Open |

❌ **Failed to create:**
- [Summary] — [error reason]
```

---

### 3. Final Completion Report

After all publishing actions complete:

```
**🎯 Workflow Complete — Here's what was created:**

📄 Local file: [file path]
🌐 Confluence: [URL] (if published)
📋 Jira: [list of issue keys] (if created)

You can reference these at any time, and update the Confluence page as the feature evolves.
```

---

## FAILURE HANDLING

- **MCP unavailable**: "Atlassian MCP not available. Here is the document content for manual publishing: [content]"
- **Confluence page creation fails**: Retry once, then provide content for manual copy-paste
- **Jira story creation fails for individual story**: Skip and note in report, continue with others
- **User selects [S] Skip**: Acknowledge and complete workflow with local file only

---

## SUCCESS METRICS

✅ User presented with clear publishing options before any action is taken
✅ Existing Confluence page detected and updated (not duplicated)
✅ Page created under correct parent (Feature Grooming) with correct labels
✅ Jira issues created with proper format, labels, and epic linkage
✅ Failures handled gracefully with manual fallback content provided
✅ Final completion report shows all created artifacts with URLs/keys
