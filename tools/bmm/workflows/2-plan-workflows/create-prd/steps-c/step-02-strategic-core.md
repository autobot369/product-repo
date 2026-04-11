---
name: 'step-02-strategic-core'
description: >
  Single-pass Strategic Core intake. Merges Problem Statement, Target User, and
  Success Metrics into one dense structured prompt. Replaces steps 02, 02b, 02c,
  and 03 when prd_intake_mode=strategic-core in config.yaml.

# File References
nextStepFile: './step-04-journeys.md'
outputFile: '{planning_artifacts}/prd.md'

# Config reference
strategicCoreTemplate: '{project-root}/tools/bmm/config.yaml#strategic_core_template'

# Task References
advancedElicitationTask: '~/.claude/bmm/core/workflows/advanced-elicitation/workflow.xml'
partyModeWorkflow: '~/.claude/bmm/core/workflows/party-mode/workflow.md'
---

# Step 2: Strategic Core (Single-Pass Intake)

**Progress: Step 2 of 9** — replaces steps 02 + 02b + 02c + 03
Next: User Journey Mapping (Step 4)

## STEP GOAL

Present a single dense structured intake form that captures Problem Statement,
Target User, and Success Metrics in one pass. Pre-fill from any loaded input
documents (brief, research). John reviews and completes in one shot.
Generate Executive Summary + Success Criteria sections directly from the filled form.

---

## MANDATORY EXECUTION RULES (READ FIRST)

- 🛑 NEVER ask the five-question discovery sequence — this step replaces it entirely
- 📖 Read this complete file before taking any action
- 📋 YOU ARE A FACILITATOR presenting a form, not running a conversation
- ✅ Pre-fill every field you can derive from loaded input documents
- 🚫 FORBIDDEN to route through step-02-discovery, step-02b, step-02c, or step-03
- ✅ ALWAYS communicate in `{communication_language}`

---

## EXECUTION SEQUENCE

### 1. Load the Strategic Core Template

Read `{strategicCoreTemplate}` from config.yaml.
Extract the `strategic_core_template` block — this is the intake structure.

### 2. Pre-fill from Input Documents

Scan all documents loaded in step-01 (brief, research, brainstorming, project docs).
For each field in the template, extract any matching signal:

| Template field | Look for in input docs |
|----------------|------------------------|
| `problem_statement.what` | Problem framing, pain points, opportunity statements |
| `problem_statement.who` | User segments, personas, audience definitions |
| `problem_statement.why_now` | Market timing, competitor signals, urgency drivers |
| `problem_statement.current_workaround` | Workarounds, friction notes, "as-is" flows |
| `target_user.segment` | Persona names, user types, cohort definitions |
| `target_user.context` | Journey stages, touchpoints, use-case contexts |
| `target_user.job_to_be_done` | JTBD statements, underlying goals, "help me..." language |
| `target_user.pain_intensity` | Severity language: critical / blocker / frustration / nice-to-have |
| `success_metrics.primary_kpi` | KPIs, OKRs, north-star metrics with baselines |
| `success_metrics.secondary_kpis` | Supporting metrics, guardrail metrics |
| `success_metrics.cr_impact` | Conversion rate hypotheses, funnel impact estimates |
| `success_metrics.aov_impact` | AOV, basket size, upsell hypotheses |
| `success_metrics.time_to_validate` | Launch timelines, measurement windows |

Mark pre-filled fields with `✓ (from [source filename])`.
Leave blank fields empty — they become targeted follow-up questions in step 3.

### 3. Present the Strategic Core Form

Present the form to the user as a single block. Use this exact structure:

---

**Strategic Core — {project_name}**
*Review pre-filled fields, complete any blanks, and confirm when ready.*

**Problem Statement**
```
What (friction/gap):     [pre-filled or blank]
Who (segment):           [pre-filled or blank]
Why now (urgency):       [pre-filled or blank]
Current workaround:      [pre-filled or blank]
```

**Target User**
```
Segment:                 [pre-filled or blank]
Context (where/when):   [pre-filled or blank]
Job-to-be-done:          [pre-filled or blank]
Pain intensity:          [low | medium | high | critical]
```

**Success Metrics**
```
Primary KPI:             [metric — baseline → target]
Secondary KPIs:          [2–3 metrics]
CR impact hypothesis:    [directional, e.g. +2–4% checkout CR]
AOV impact hypothesis:   [directional]
Time to validate:        [e.g. 6 weeks post-launch]
```

---

Ask only for blank fields — do not re-ask pre-filled fields unless the user
explicitly wants to revise them:

> "I've pre-filled [N] fields from your [brief/research/docs].
> The following fields need your input: [list blank field names only].
> Complete these and I'll generate the full Strategic Core in one pass."

### 4. Resolve Blank Fields

For each blank field, ask a single targeted question — not an open-ended
discovery conversation. Example:

- `why_now` blank → "What's the urgency signal or market timing for this now?"
- `primary_kpi` blank → "What's the single metric that would tell you this worked, and what's the baseline?"
- `pain_intensity` blank → "How severe is this pain for the user — does it block them, frustrate them, or just slow them down?"

Halt after each question and wait for the answer. Do not batch questions.

### 5. Generate PRD Sections from the Completed Form

Once all fields are confirmed, generate three PRD sections in a single pass.
Do not ask for separate approval between sections — present all three together.

#### Section A — Executive Summary

```markdown
## Executive Summary

{problem_statement.what}. This affects {target_user.segment} when
{target_user.context}. Their underlying goal is {target_user.job_to_be_done}.
{problem_statement.current_workaround} is the current workaround, indicating
{problem_statement.why_now}.

### What Makes This Special

[Synthesised from input docs or flagged for user input if no differentiator signal found]

## Project Classification

- **Target segment:** {target_user.segment}
- **Pain intensity:** {target_user.pain_intensity}
- **Context:** {target_user.context}
```

#### Section B — Success Criteria

```markdown
## Success Criteria

### Primary KPI
{success_metrics.primary_kpi}

### Supporting KPIs
{success_metrics.secondary_kpis — one bullet per metric}

### Business Impact Hypotheses
- CR: {success_metrics.cr_impact}
- AOV: {success_metrics.aov_impact}

### Validation Window
{success_metrics.time_to_validate}
```

#### Section C — Strategic Core (machine-readable block)

Append a YAML front-matter style block at the end of the document for
downstream agent consumption (epic decomposition, story generation):

```yaml
strategic_core:
  problem: "{problem_statement.what}"
  segment: "{target_user.segment}"
  jtbd: "{target_user.job_to_be_done}"
  primary_kpi: "{success_metrics.primary_kpi}"
  cr_hypothesis: "{success_metrics.cr_impact}"
  aov_hypothesis: "{success_metrics.aov_impact}"
```

### N. Present MENU OPTIONS

Present all three generated sections for review, then display menu:

> "Here's the Strategic Core for your PRD. Review the three sections above —
> Executive Summary, Success Criteria, and the machine-readable block.
> What would you like to do?"

Display: `[A] Advanced Elicitation  [P] Party Mode  [C] Continue to User Journeys (Step 4 of 9)`

#### Menu Handling Logic

- **A**: Run `{advancedElicitationTask}` against the Strategic Core content.
  Process enhanced output. Ask: "Accept these improvements? (y/n)".
  On yes: update all three sections and redisplay menu.
  On no: keep originals and redisplay menu.
- **P**: Run `{partyModeWorkflow}` against the Strategic Core content.
  Process collaborative improvements. Ask: "Accept these changes? (y/n)".
  On yes: update sections and redisplay menu.
  On no: keep originals and redisplay menu.
- **C**: Append all three sections to `{outputFile}`. Update frontmatter:
  - Add `step-02-strategic-core` to `stepsCompleted`
  - Mark skipped: `stepsSkipped: [step-02-discovery, step-02b-vision, step-02c-executive-summary, step-03-success]`
  - Then read fully and follow: `{nextStepFile}`
- **Any other**: Answer and redisplay menu.

---

## CRITICAL STEP COMPLETION NOTE

ONLY when **[C]** is selected AND all three sections are appended to `{outputFile}`
AND frontmatter is updated with `stepsCompleted` and `stepsSkipped` will you read
fully and follow `{nextStepFile}` to begin User Journey Mapping.

---

## SUCCESS METRICS

✅ Template loaded from config.yaml and pre-filled from input documents
✅ Only blank fields prompted — no re-asking of pre-filled values
✅ All three sections generated in a single pass from the completed form
✅ `stepsSkipped` recorded in frontmatter for traceability
✅ Machine-readable `strategic_core` YAML block appended to document
✅ A/P/C menu presented and handled correctly

## FAILURE MODES

❌ Running the multi-turn discovery conversation (step-02 behaviour) — this is FORBIDDEN
❌ Asking for problem statement, vision, and metrics in separate turns
❌ Generating sections one at a time with separate approval gates
❌ Not recording `stepsSkipped` in frontmatter
❌ Proceeding to `{nextStepFile}` without user selecting [C]
❌ Leaving the machine-readable `strategic_core` YAML block out of the document
