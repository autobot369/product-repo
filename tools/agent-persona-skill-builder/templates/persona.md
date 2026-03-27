# Persona Template — Annotated

Personas are **user archetypes** — reference profiles used during journey mapping, story writing, usability reviews, and synthetic LLM-based user testing. They are NOT agent files. No activation block, no menu, no XML.

---

## Token budget breakdown

| Section | Typical tokens | Notes |
|---------|---------------|-------|
| Frontmatter | ~15 | Fixed |
| Identity | ~60–80 | 3–4 sentences |
| Goals | ~20–30 | New — drives acceptance criteria |
| Traits + Pain Points | ~60–80 | Bullet lists |
| Trigger Phrases | ~30–50 | New — enables synthetic testing |
| Tech profile + Usage | ~20 | Fixed structure |
| **Total** | **~200–275** | Target range |

---

## Template

```markdown
---
name: "{slug}"                          # matches filename without .md
description: "{≤20-word description}"   # who this person is and what they represent
type: persona
group: "{group-folder}"                 # e.g. shoppers, store-staff, ops-users, enterprise-admins
---

# {icon} {FirstName} — {Title}
**Segment:** {group label}  |  **Tech Savvy:** {1–5}  |  **Primary device:** {device}

---

## Identity

<!--
  3–4 sentences: background, context, mental model.
  Where do they work / shop? What do they know cold? What drives their decisions?
  Avoid: demographic details that don't affect product behaviour (age, hometown, etc.)
  Good:  "Jordan manages a 12-person store team and evaluates tools by one standard:
          does it work when the queue is 8 deep and the Wi-Fi is flaky?"
-->
{3–4 sentences}

## Goals

<!--
  2–4 bullets: what this persona is actively trying to accomplish.
  State as outcomes, not feature requests.
  These map directly to acceptance criteria in user stories — keep them concrete.
  Bad:  "Wants a better experience."
  Good: "Get weekly reporting done without manual data entry."
        "Know immediately when a system change breaks her team's workflow."
-->
- {Goal one — outcome, not feature}
- {Goal two}
- {Goal three}

## Core Traits

<!--
  4–6 bullets, ≤12 words each.
  Observable behaviours, not personality adjectives.
  Bad:  "Enthusiastic and detail-oriented."
  Good: "Decides by peer review count — skips product descriptions entirely."
-->
- {Trait one}
- {Trait two}
- {Trait three}
- {Trait four}

## Pain Points

<!--
  3–5 bullets, ≤12 words each.
  Friction they experience today. Workarounds they've invented.
  These should be specific enough to map to product decisions.
  Bad:  "Finds the app confusing sometimes."
  Good: "Can't compare more than two products side by side — screenshots to Notes."
-->
- {Pain point one}
- {Pain point two}
- {Pain point three}

## Trigger Phrases

<!--
  3–5 verbatim phrases this persona actually says — in their own voice.
  This is the highest-signal section for:
    • Synthetic user testing (LLM plays this persona and uses these phrases)
    • Chatbot / support conversation design (what triggers to handle)
    • UX copy validation (does the UI speak their language?)
    • Acceptance criteria ("system responds correctly when user says X")
  Bad:  "Asks about reporting features."
  Good: "Can I export this to Excel?" / "Where's the webhook documentation?"
-->
- *"{Verbatim phrase one}"*
- *"{Verbatim phrase two}"*
- *"{Verbatim phrase three}"*

## Technology Profile

<!--
  Tech Savvy: 1 (needs hand-holding) → 5 (power user, CLI-comfortable).
  Use numeric so personas can be compared and filtered in tables.
-->
- **Tech Savvy:** {1–5} — {one-sentence elaboration}
- **Primary devices:** {e.g. iPhone, shared iPad POS terminal, laptop}
- **Tool usage:** {e.g. Uses CLI where possible. Avoids UI for repetitive tasks.}

## Usage

<!--
  One-line invocation example. Shows a PM exactly how to use this persona.
  For synthetic testing: describe what scenario to run.
-->
```
Use @.claude/personas/{group}/{slug}.md — {one-line task description}
```

<!--
  Synthetic testing example (optional — add when persona will be used for LLM simulation):
-->
For synthetic testing: ask Claude to roleplay as {FirstName} and respond to onboarding prompts.
Use their trigger phrases as starting inputs. Flag any response that contradicts their goals or traits.
```

---

## Tech Savvy scale

| Score | Profile |
|-------|---------|
| 1 | Needs step-by-step guidance; avoids anything unfamiliar |
| 2 | Comfortable with standard UI; confused by non-obvious patterns |
| 3 | Learns new tools independently; uses search/help docs |
| 4 | Power user; customises settings; prefers shortcuts |
| 5 | Developer-comfortable; uses CLI, APIs, webhooks without hesitation |

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Writing traits as adjectives ("organized", "tech-savvy") | Write as observable behaviours ("Books meetings 24h in advance; declines without agenda") |
| Pain points too vague ("finds it slow") | Make specific and product-mappable ("Timeout on product search after 8s — has to re-enter query") |
| Goals written as feature requests ("wants a filter") | Write as outcomes ("Find the right product in under 60 seconds without scrolling") |
| Trigger phrases are paraphrased | Quote verbatim — the specific words matter for UX copy and chatbot design |
| Identity > 4 sentences | Cut generic background; keep only what affects product behaviour |
| Adding activation/menu structure | Personas are reference docs only — no XML, no activation |
