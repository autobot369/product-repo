# Skill Template — Annotated

Skills define **what Claude executes** — a step-by-step workflow triggered by a slash command. Unlike agents (which set behavioural framing), skills are purely procedural.

> **Two types of skills exist in this library:**
> - **Slash-command skills** (this template) — executable Claude Code playbooks invoked via `/command`
> - **Capability registry** — documents what the *product and team* can do; see `capability-registry.md` template

---

## Token budget breakdown

| Section | Typical tokens | Notes |
|---------|---------------|-------|
| Frontmatter | ~25–35 | Now includes dependencies |
| Invocation block | ~20–40 | Scales with param count |
| Steps | ~100–200 | Your main variable |
| Output + guidelines | ~30–50 | Keep tight |
| **Total** | **~175–325** | Target range |

The frontmatter `description` is disproportionately important — it is what Claude reads when deciding whether to invoke this skill. Make it precise and complete.

---

## Template

```markdown
---
description: {≤30-word precise trigger description — what this skill does, when to use it, key inputs}
dependencies:           # external services this skill calls — documents runtime requirements
  - {Confluence: reads space, writes page}
  - {Jira: creates issues, assigns sprint}
  - {Anthropic API: optional classifier fallback}
---

# /{slash-command} — {Skill Display Name}

## Invoke

<!--
  Show only the parameters the user must or may provide.
  (optional) suffix for non-required params.
  Don't explain what each param does — the name should be self-evident.
-->
```
/{slash-command}
{Param one}: [{description}]
{Param two}: [{description}]  (optional)
```

## 1 — {Step title: verb + object, ≤6 words}

<!--
  Each step: 1 imperative sentence, or a table for branching/decision logic.
  No preamble. No "In this step you will..."
  Start immediately with what to do.

  Bad:  "In this step, you will need to search the Confluence space for any pages
         related to the topic that the user has provided in order to understand..."
  Good: "Search the configured Confluence space for existing research on the topic — read 3–5 most relevant pages."

  Use tables when step has conditional logic:
-->

| Signal | Action |
|--------|--------|
| PRD URL provided | Fetch page — extract goal, personas, ACs, constraints |
| No PRD | Search space with epic key — read 5–8 pages — list sources in report |

## 2 — {Step title}

{Imperative sentence or table}

## 3 — {Step title}

{Imperative sentence or table}

<!--  Add steps as needed. Typical skill: 3–6 steps. -->

## Output

<!--
  One paragraph or bullet list: exactly what the skill produces.
  If it writes to Confluence/Jira/files, say so here.
-->
{Output description}

**Side effects:** {e.g. "Creates Confluence page with labels: research, pm-agent-generated." or "None."}

## Guidelines

<!--
  4–6 bullets, ≤12 words each. Hard constraints and error-handling rules.
  Not suggestions — these are the rules Claude must follow.
  Bad:  "It is generally a good idea to try to avoid creating duplicate entries..."
  Good: "Never create a Jira story that already exists — check first."
-->
- {Constraint one}
- {Constraint two}
- {Constraint three}
- {Constraint four}
```

---

## When to use tables vs prose in steps

| Use a table when... | Use prose when... |
|--------------------|------------------|
| Step has 2+ conditional branches | Step is a single linear action |
| Choosing between templates or routing rules | Fetching or reading a resource |
| Mapping signals to outputs | Generating content |
| Report structure definition | Posting/publishing to external system |

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Frontmatter description is vague ("Helps with research") | Be specific: what topic, what output, what inputs trigger it |
| Missing `dependencies` | Every skill calling Confluence/Jira/external APIs must list them — enables debugging and permission auditing |
| Steps written as paragraphs | One sentence per step; use tables for branching |
| Guidelines section > 6 bullets | Hard constraints only — remove "nice to have" suggestions |
| Repeating the persona from agents | Skills have no persona section — they are procedural only |
| Side effects buried in step text | Consolidate all external writes in the Output section |
