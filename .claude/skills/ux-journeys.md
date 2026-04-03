---
description: "Maps user journeys and embeds them inline into the PRD's Functional Requirements. No separate UX doc. Run during Phase 02 alongside /create-prd."
version: "1.1.0"
last_updated: "2026-04-02"
bmm_phase: "02_Solutioning_Sprint"
bmm_step: "ux_journeys_inline"
bmm_agent: ux-designer
bmm_runs: standalone_or_orchestrated
bmm_reads:
  - "tools/bmm/output/briefs/product-brief.md"
  - "tools/bmm/output/research/research-findings.md"
  - "docs/user-journeys/"
output_mode: inline
output_target_file: "tools/bmm/output/prds/final-prd.md"
output_target_section: "Functional Requirements"
output_contract:
  required_per_journey:
    - journey_name
    - persona
    - trigger
    - happy_path_steps
    - failure_states
    - design_notes
  min_journeys: 2
handoff_writes:
  - key: ux_journeys_complete
    value: true
dependencies:
  confluence:
    actions: [search, read]
    required: false
---

# /ux-journeys — UX Journey Mapping (Inline)

## Invoke

```
/ux-journeys
PRD: tools/bmm/output/prds/final-prd.md   (path to PRD being authored)
Feature: [initiative name — used to scope journey discovery]
Personas: [optional — comma-separated persona names to focus on]
```

Or in orchestrated mode — Optimus Prime passes context directly, no manual invocation needed.

## Standalone mode — no PRD exists yet

If `final-prd.md` does not exist at the specified path, Arcee writes a standalone journey document:

```
tools/bmm/output/prds/ux-journeys-draft.md
```

At completion, Arcee prompts:
> "Journeys saved to `ux-journeys-draft.md`. Run `/create-prd` next — Optimus Prime can incorporate these directly into the PRD's Functional Requirements section."

This draft is not counted as the `ux_journeys_complete` handoff signal — only inline PRD embedding sets that flag.

## 1 — Load context

Read in order:
1. `tools/bmm/output/briefs/product-brief.md` — extract target user segment, JTBD, pain intensity
2. `tools/bmm/output/research/research-findings.md` — extract behavioural signals and competitor journey patterns
3. `docs/user-journeys/` — scan all existing funnel-stage docs for journey precedents relevant to this feature
4. Confluence (if available) — search for design system docs, prior UX flows, and pattern library pages

Identify which funnel stage this feature primarily lives in:
- **Front Funnel** — discovery, browse, search, recommendations
- **Mid Funnel** — PDP, comparison, wishlist, add-to-cart
- **Bottom Funnel** — checkout, payment, order confirmation
- **Loyalty** — post-purchase, returns, account, repeat purchase

## 2 — Define journeys

For each primary persona identified in the brief, map at minimum:

### Journey structure (per journey)

```markdown
### Journey: [Journey Name]
**Persona:** [segment name from brief]
**Funnel stage:** [Front | Mid | Bottom | Loyalty]
**Trigger:** [what causes the user to start this flow]
**Entry point:** [screen or surface where the journey begins]

#### Happy Path
| Step | User action | System response | Design note |
|------|-------------|-----------------|-------------|
| 1 | [what user does] | [what product does] | [UX principle or constraint] |
| ... | | | |

#### Failure States
| Trigger | Current experience | Ideal experience |
|---------|-------------------|------------------|
| [e.g. network error] | [blank screen] | [inline retry with context preserved] |

#### Edge Cases
- [e.g. returning user with saved state — skip step 2]
- [e.g. guest user — prompt account creation post-confirmation only]
```

Map at minimum:
- 1 happy path per primary persona
- All failure and empty states
- At least 2 edge cases per journey

## 3 — Embed into PRD

Open `tools/bmm/output/prds/final-prd.md`. Locate the `## Functional Requirements` section (create it if missing). Append a `### User Journeys` subsection with all mapped journeys.

**Do not overwrite any content Optimus Prime has already written.** Append only to the designated subsection. If the section already has content, review it first and extend rather than replace.

Format:

```markdown
### User Journeys

> Authored by Arcee (UX Designer) — embedded inline per BMM Phase 02 protocol.
> Reference: docs/user-journeys/[FunnelStage]/ for canonical journey patterns.

[Journey maps go here]
```

## 4 — Design principles applied

For every journey, validate against Arcee's core principles:

| Principle | Check |
|---|---|
| Discovery first | Can the user find what they need in ≤ 3 taps from the home screen? |
| Mobile-first | Every step works on a 375px viewport without horizontal scroll |
| Personalisation depth | Does the journey adapt based on known user state (logged in, prior purchase)? |
| Quality bar | Would a discerning user be proud of each screen transition? |

Flag any journey step that fails a check — add a design note explaining the trade-off.

## 5 — Review

Present the embedded journeys to the user. Ask:
- "Does this cover all the flows the PRD needs to be implementable?"
- "Any personas or edge cases I've missed?"

Do not proceed to gate until user confirms.

## Output

User journeys embedded directly into `tools/bmm/output/prds/final-prd.md` under `## Functional Requirements → ### User Journeys`. No separate file is produced.

**In orchestrated mode:** Arcee works interleaved with Optimus Prime — Optimus Prime authors requirements top-down, Arcee appends journeys bottom-up into the same section. Both signal complete before the Technical Readiness gate runs.

## Failure Modes

| Condition | Behaviour |
|---|---|
| `final-prd.md` does not exist | Write standalone `ux-journeys-draft.md` (see Standalone mode section above) — do not fail silently |
| Brief not found | Ask user for key context — persona name, JTBD, and pain intensity — before mapping journeys |
| Journey maps `min_journeys: 2` cannot be met from inputs | Ask for a second persona or feature area to map before completing |
| PRD already has a populated User Journeys section | Review existing journeys first — extend rather than replace; confirm with user before overwriting any content |
| Confluence unavailable | Proceed without design system context — note "No Confluence design system context loaded" in design notes |

## Guidelines

- Never produce a standalone UX design document — inline-only in orchestrated mode.
- Reference `docs/user-journeys/` as the canonical pattern library — don't invent patterns that conflict with existing funnel flows.
- "Mobile-first" means designed for mobile, gracefully enhanced for desktop — not "desktop with a responsive breakpoint."
- Failure states are not optional — every happy path must have at least one documented failure state.
- Calibrate explanation depth to `{user_skill_level}` from config:
  - `beginner` — explain the journey mapping format with an example before starting; confirm persona choices interactively
  - `intermediate` — map all journeys, present for review
  - `expert` — produce all journeys in one pass, flag principle violations, ask for a single confirmation
