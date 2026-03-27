# 🛠️ Skill & Capability Matrix
> **Status:** Active | **Last Updated:** 2026-03-27

Slash-command skills define what Claude executes — step-by-step playbooks invoked via a `/command`. This document maps product capabilities, team skill ownership, and the tooling stack.

---

## Product Capabilities (Functional)

* **Skill: PRD Creation**
  * *Description:* Generates a fully structured PRD in Confluence from a minimal brief.
  * *Owner:* AG-PM (John)
  * *Slash command:* `/create-prd`
  * *Dependencies:* Confluence (search, read, create/update page, add labels), Jira (epic reference)

* **Skill: User Story Generation**
  * *Description:* Creates Jira user stories from a PRD URL or Confluence context search.
  * *Owner:* AG-PM (John) / AG-SM (Bob)
  * *Slash command:* `/user-stories`
  * *Dependencies:* Confluence (search, read pages), Jira (search, create issues, get sprints, assign sprint)

* **Skill: Market Research**
  * *Description:* Produces a structured market research report and publishes it to Confluence.
  * *Owner:* AG-ANALYST (Mary)
  * *Slash command:* `/market-research`
  * *Dependencies:* Confluence (search, read, create page, add labels), Web search

* **Skill: Confluence Coverage Audit**
  * *Description:* Scans a Confluence space and bulk-creates Jira stories for undocumented features.
  * *Owner:* AG-PM (John) / AG-SM (Bob)
  * *Slash command:* `/confluence-user-stories`
  * *Dependencies:* Confluence (read space, read pages), Jira (search, create issues, link epic, add labels)

---

## Team Skills (Operational)

| Skill | Lead | Backup | Documentation |
| :--- | :--- | :--- | :--- |
| PRD Writing | AG-PM (John) | AG-ANALYST (Mary) | [create-prd.md](create-prd.md) |
| Market Research | AG-ANALYST (Mary) | AG-PM (John) | [market-research.md](market-research.md) |
| Story Preparation | AG-SM (Bob) | AG-PM (John) | [user-stories.md](user-stories.md) |
| Coverage Auditing | AG-SM (Bob) | AG-PM (John) | [confluence-user-stories.md](confluence-user-stories.md) |
| Architecture Design | AG-ARCH (Winston) | — | [agents/architect.md](../agents/architect.md) |
| UX Design | AG-UX (Sally) | — | [agents/ux-designer.md](../agents/ux-designer.md) |

---

## Tooling Stack

* **LLM:** claude-sonnet-4-6 — default model for all agents and skills (configured in `tools/bmm/config.yaml`)
* **PM Workflow Engine:** BMM (`tools/bmm/core/workflow.xml`) — orchestrates multi-step agent workflows
* **Knowledge Base:** `docs/` (MkDocs) + Confluence space (via Atlassian MCP) — agents read both for context
* **Issue Tracking:** Jira (via Atlassian MCP) — story creation, sprint assignment, epic linking
* **Design:** Figma (via Figma MCP) — referenced in PRDs; linked after UX kickoff
* **Deployment:** MkDocs + GitHub Pages (`mkdocs gh-deploy`) — publishes `docs/` as a static site

---

## Adding skills

A skill file must define:
1. **Frontmatter** — `description` (≤30 words) and `dependencies` (every external service called)
2. **Invoke** — parameters the user provides
3. **Steps** — numbered `## N — {verb phrase}`, each a single imperative sentence or decision table
4. **Output** — exact deliverable + `**Side effects:**` line for any external writes
5. **Guidelines** — 4–6 hard constraints, ≤12 words each

Generate with: `python tools/agent-persona-skill-builder/builder.py --type skill`

## See also

- [.claude/agents/README.md](../agents/README.md) — agent registry and interaction logic
- [tools/pm-workers/README.md](../../tools/pm-workers/README.md) — CLI runner for programmatic skill execution
- [templates/skill.md](../../tools/agent-persona-skill-builder/templates/skill.md) — skill file template
- [templates/capability-registry.md](../../tools/agent-persona-skill-builder/templates/capability-registry.md) — this document's template
