---
title: "SME Capital Advantage Navigator — UX Component Library"
product: "SME Capital Advantage Navigator"
date: 2026-04-03
status: draft
agent: "Arcee (ux-designer)"
bmm_phase: "02_Solutioning_Sprint"
version: "1.0"
related: "docs/specs/sme-capital-advantage-style-guide.md"
---

# SME Capital Advantage Navigator — UX Component Library

> **Status:** Draft — companion to the Style Guide. Defines the reusable UI components specific to this product. Each component maps to one or more Functional Requirements in the PRD. Engineering should implement these as the design system foundation before building feature screens.
>
> Figma component library: *Link to be added after UX kickoff.*

---

## Component Index

| Component | Maps to FR | Priority |
|---|---|---|
| [MyInfo Connect Entry](#myinfo-connect-entry) | FR-01, FR-09 | P0 — Calculator landing (Branch B entry) |
| [MyInfo Data Review Card](#myinfo-data-review-card) | FR-09 | P0 — Post-OAuth data display |
| [MyInfo Connection Status Badge](#myinfo-connection-status-badge) | FR-09 | P0 — Dashboard header |
| [Existing Grants Insight Card](#existing-grants-insight-card) | FR-09, FR-04 | P0 — Branch B results + Navigator dashboard |
| [Financial Signal Card](#financial-signal-card) | FR-01, FR-06 | P0 — Calculator results screen |
| [Eligibility Badge](#eligibility-badge) | FR-04, FR-05 | P0 — Grant match list |
| [Grant Match Card](#grant-match-card) | FR-04 | P0 — Grant eligibility engine |
| [FI Rate Comparison Card](#fi-rate-comparison-card) | FR-05 | P0 — Loan routing |
| [Document Upload Zone](#document-upload-zone) | FR-02 | P0 — Document Agent |
| [OCR Confidence Indicator](#ocr-confidence-indicator) | FR-02 | P0 — Document Agent review |
| [Blurred Preview Gate](#blurred-preview-gate) | FR-07 | P0 — Freemium conversion |
| [WACC Impact Panel](#wacc-impact-panel) | FR-06 | P1 — Retention |
| [Brown Discount Risk Card](#brown-discount-risk-card) | FR-06 | P1 — Retention |
| [Progress Stage Indicator](#progress-stage-indicator) | FR-02, FR-04 | P1 — Onboarding flow |
| [Consent Modal](#consent-modal) | FR-05 | P0 — Loan routing |
| [Application Status Pill](#application-status-pill) | FR-05 | P1 — My applications view |
| [Formula Version Footer](#formula-version-footer) | FR-01 | P0 — Calculator |
| [Eligibility Gap Card](#eligibility-gap-card) | FR-04 | P1 — Not yet eligible path |
| [SEFR Alignment Badge](#sefr-alignment-badge) | FR-01 | P0 — Calculator results (trust signal) |

---

## MyInfo Connect Entry

**Purpose:** Dual-path entry point on the Calculator landing screen. Presents Branch A (Quick Estimate) and Branch B (MyInfo Business connection) as co-equal options. The most important acquisition screen in the product.

**Maps to:** FR-01 AC-02, FR-09 AC-01

### Anatomy — Landing Screen (above fold, 375px)

```
┌──────────────────────────────────────────────────────────────────────┐
│  Your competitors already know how much the carbon tax               │
│  is costing them. Do you?                                            │
├─────────────────────────────┬────────────────────────────────────────┤
│  Quick Estimate             │  [Singpass logo] Connect MyInfo        │
│  3 questions, 2 minutes     │  Business                              │
│                             │  ✦ More accurate                       │
│  [Get started →]            │  Uses your ACRA-verified company data  │
│                             │                                        │
│                             │  [Connect MyInfo Business →]           │
├─────────────────────────────┴────────────────────────────────────────┤
│  3,200 Singapore SMEs have used Navigator to find green finance.     │  ← social proof
└──────────────────────────────────────────────────────────────────────┘
```

### Mobile layout (375px — single column)

On mobile, Branch B ("Connect MyInfo Business") appears **above** Branch A ("Quick Estimate") — MyInfo is the preferred path and gets first position on mobile where the Singpass app makes OAuth friction minimal.

```
┌──────────────────────────────────────────────────────┐
│  Hero headline (2 lines max on 375px)                │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │  [Singpass logo] Connect MyInfo Business       │  │  ← PRIMARY (mobile top)
│  │  Get exact figures using your ACRA data        │  │
│  │  ✦ More accurate                               │  │
│  └────────────────────────────────────────────────┘  │
│                                                      │
│  ─────────── or ───────────                          │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │  Quick Estimate — 3 questions                  │  │  ← SECONDARY (mobile bottom)
│  │  Get an estimate in 2 minutes                  │  │
│  └────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

### MyInfo Button Styling

> **Important:** The Singpass/MyInfo branding guidelines require specific treatment of the Singpass logo and MyInfo wordmark. Refer to Singpass Partner Design Guide (obtain from Singpass developer portal at onboarding).

| Property | Value |
|---|---|
| Button background | Singpass red (`#B20000`) — as per Singpass brand guideline; this is the ONE exception to the "no bank colour" rule |
| Button text | White, Inter 600, 14px |
| Singpass logo | Official SVG mark from Singpass partner kit — left-aligned in button |
| "✦ More accurate" badge | `color-signal-gain-bg` background, `color-signal-gain` text, 11px 600 — appears above button |

### States

| State | Visual |
|---|---|
| Default | Both options visible; MyInfo has "More accurate" badge |
| Branch B in progress (OAuth redirect pending) | "Connect MyInfo Business" button shows loading spinner; Branch A dims but remains accessible |
| Branch B failed (OAuth error) | Banner appears: "MyInfo connection failed — try the Quick Estimate below." Branch A highlighted. |
| Branch B success (returned from Corppass) | Transition to MyInfo Data Review Card — Calculator landing is replaced |

### Rules
- Never hide one option to force the other — both must be co-equal on first render
- Never label Branch A as "inferior" or Branch B as "premium" — frame as "more accurate", not "better"
- The MyInfo button must use Singpass-approved branding — do not redesign the button colour or logo placement
- Social proof line (3,200 SMEs) updates dynamically from platform analytics — do not hardcode

---

## MyInfo Data Review Card

**Purpose:** Shown immediately after successful Corppass OAuth redirect. Displays all ACRA/MTI data retrieved and builds trust through transparency before the user proceeds to remaining manual inputs.

**Maps to:** FR-09 AC-03, AC-05

### Anatomy

```
┌──────────────────────────────────────────────────────────────────────┐
│  ✓ Connected to MyInfo Business                                      │
│  Retrieved from ACRA and MTI on 3 April 2026                        │
├──────────────────────────────────────────────────────────────────────┤
│  Company            [Entity Name Pte Ltd]         ACRA ✓             │
│  UEN                201912345A                    ACRA ✓             │
│  Sector             Manufacturing (SSIC 2511)     ACRA ✓             │
│  Revenue (FY2024)   S$2,400,000                   ACRA ✓             │
│  Paid-up Capital    S$500,000                     ACRA ✓             │
│  Existing Grants    EEG Base Tier — Approved      MTI  ✓             │
├──────────────────────────────────────────────────────────────────────┤
│  ⚠ Revenue data is from FY2024 (filed Jan 2025). If your revenue    │
│  has changed significantly, you can adjust below.        [Adjust]    │
├──────────────────────────────────────────────────────────────────────┤
│  Everything look right?              [Yes, continue →]  [Edit]       │
└──────────────────────────────────────────────────────────────────────┘
```

### Rules
- Every field shows its source agency (ACRA / MTI) with a green verified tick
- Financial year displayed for all financial figures — never show a bare number without a period
- Staleness warning shown if financial period end date is >12 months ago — amber banner, non-blocking
- "Edit" button allows user to override any field with manual entry — override is tagged `source: manual_override` in the event log
- "Yes, continue" advances to the 2-field manual input screen (electricity spend + export markets)
- Card must not be skippable — user must explicitly confirm or edit before proceeding

---

## MyInfo Connection Status Badge

**Purpose:** Persistent indicator in the Navigator dashboard header showing MyInfo connection state. Present on every authenticated screen for MyInfo-connected profiles.

**Maps to:** FR-09 AC-11

### Anatomy — Connected

```
 [Singpass mark]  MyInfo Connected  ·  ACRA data: 3 Apr 2026  [Refresh]
```

### Anatomy — Not Connected

```
 [link icon]  Connect MyInfo Business for exact eligibility scoring  →
```

### States

| State | Visual | Behaviour |
|---|---|---|
| Connected | Green tick + "MyInfo Connected" + retrieval date + Refresh link | Refresh re-triggers OAuth to update ACRA data |
| Not connected | Amber link with prompt to connect | Clicking opens MyInfo Connect Entry modal (doesn't leave the page) |
| Refresh in progress | Spinner + "Updating via MyInfo…" | Non-blocking — user can continue using Navigator |
| Refresh failed | "MyInfo refresh failed — using data from [date]" | Non-blocking amber banner; data remains from last successful fetch |

### Rules
- Always visible in dashboard header for authenticated users
- "Not connected" state shown with urgency but not alarm — no red; amber is sufficient
- Refresh is user-initiated only — never auto-refresh without user action (PDPA / Corppass consent requirement)

---

## Existing Grants Insight Card

**Purpose:** Surfaces the user's MTI-verified grant history and the next logical instrument to apply for. Exclusive to MyInfo-connected profiles. Appears on the Branch B Calculator results screen and in the Navigator dashboard.

**Maps to:** FR-09 AC-09, FR-04

### Anatomy

```
┌──────────────────────────────────────────────────────────────────────┐
│  📋  Your Verified Grant History                     MTI via MyInfo  │
├──────────────────────────────────────────────────────────────────────┤
│  ✓  EEG Base Tier            Approved    S$45,000    2024            │
│  ✓  SME SRP                  Approved    S$8,500     2023            │
├──────────────────────────────────────────────────────────────────────┤
│  Based on your grant history, you may now qualify for:               │
│                                                                      │
│  ➜  EEG Advanced Tier        [LIKELY]   Up to S$200,000             │
│     "You've completed EEG Base — Advanced is the natural next step." │
│                                                                      │
│  ➜  EFS-Green                [POSSIBLE] Up to S$300,000             │
│     "Your energy upgrade spend may qualify for EFS co-funding."      │
└──────────────────────────────────────────────────────────────────────┘
```

### Rules
- Only shown for MyInfo-connected profiles with ≥1 existing grant in MTI data
- Existing grants shown with verified tick (✓) and MTI source label — never claim unverified data
- "Next instrument" recommendations must be grounded in actual grant scheme logic — not generic upsells
- If no existing grants: card not shown (don't display an empty "Your Grant History" panel)
- Approved amount shown only if available in MTI response — if null, show "Amount not disclosed"
- This card is the strongest trust and personalisation signal in the entire product — treat it as a premium data surface, not a sidebar widget

---

## Financial Signal Card

**Purpose:** Displays a single financial output (carbon tax cost, Brown Discount risk, or reclaim potential) from the Green Alpha Calculator and WACC model. The primary data visualisation component.

**Variants:** `cost` | `caution` | `gain`

### Anatomy

```
┌──────────────────────────────────────────────────────┐
│  [Icon]  CARD LABEL                    [variant badge]│
│                                                      │
│  S$8,100 /year                                       │  ← type-data (28px 700)
│                                                      │
│  Rising to S$14,400 by 2030                          │  ← type-body (14px 400)
│                                                      │
│  ──────────────────────────────────────────────────  │
│  Indicative estimate — formula v1.2                  │  ← type-body-small (12px)
└──────────────────────────────────────────────────────┘
```

### Variants

| Variant | Background | Left border | Icon | Usage |
|---|---|---|---|---|
| `cost` | `color-signal-cost-bg` | 3px `color-signal-cost` | TrendingUp (red) | Carbon tax cost, Brown Discount exposure |
| `caution` | `color-signal-caution-bg` | 3px `color-signal-caution` | AlertCircle (amber) | Current loan rate, partial eligibility |
| `gain` | `color-signal-gain-bg` | 3px `color-signal-gain` | TrendingDown (green) | Reclaim potential, WACC saving, Brown Discount prevention |

### States
- **Default:** Standard variant rendering
- **Loading:** Shimmer animation on data field — never show blank or 0 during calculation
- **Error:** "Could not calculate — check your inputs" — in `type-body-small`, `color-signal-cost`

### Rules
- Always label the number with a unit (S$/year, %, S$ range) — never bare numbers
- Always include the "Indicative estimate" footer on Calculator-generated cards
- Never use `cost` and `gain` on the same card
- `type-data` for the primary number; `type-body` for the supporting line; `type-body-small` for the disclaimer footer

---

## Eligibility Badge

**Purpose:** Communicates a grant or loan instrument's eligibility status at a glance. Used inside Grant Match Cards and the FI Rate Comparison.

**Variants:** `likely` | `possible` | `unlikely`

### Anatomy

```
 ┌──────────────┐
 │  ● LIKELY    │   ← type-label (11px 600 all-caps) + filled circle icon
 └──────────────┘
```

| Variant | Background | Text colour | Icon colour | Meaning |
|---|---|---|---|---|
| `likely` | `color-signal-gain-bg` | `color-signal-gain` | `color-signal-gain` | High eligibility confidence — show first in ranked list |
| `possible` | `color-signal-caution-bg` | `color-signal-caution` | `color-signal-caution` | Moderate confidence — may qualify with additional documentation |
| `unlikely` | `color-neutral-100` | `color-neutral-400` | `color-neutral-400` | Low confidence — shown last; always with gap explanation |

### Rules
- **Never use colour alone** — always pair badge colour with the text label (e.g. "Likely") for accessibility (WCAG 1.4.1)
- Badge must be visible at 11px on mobile — minimum 44px touch target for the card, not the badge itself
- `unlikely` badges should never appear in a ranked list without an accompanying gap explanation (see Eligibility Gap Card)

---

## Grant Match Card

**Purpose:** Displays a single matched grant instrument in the Grant Eligibility Engine results list. Expandable.

### Anatomy — Collapsed

```
┌──────────────────────────────────────────────────────────┐
│  [LIKELY badge]   EEG Base Tier                 [Chevron]│
│                   S$30,000 – S$200,000 estimated value   │
│                   Processed in 6–8 weeks                 │
└──────────────────────────────────────────────────────────┘
```

### Anatomy — Expanded

```
┌──────────────────────────────────────────────────────────┐
│  [LIKELY badge]   EEG Base Tier                 [Chevron]│
│                   S$30,000 – S$200,000 estimated value   │
├──────────────────────────────────────────────────────────┤
│  Eligibility checklist                                   │
│  ✓  Singapore-registered SME                             │
│  ✓  Manufacturing or commercial sector                   │
│  ✓  Qualifying energy efficiency upgrade                 │
│  ✗  Minimum S$30K capex (your profile: S$18K) ←gap      │
├──────────────────────────────────────────────────────────┤
│  Required documents                                      │
│  ☑  Utility bills (last 6 months) — uploaded            │
│  ☑  Audited P&L — uploaded                              │
│  ☐  Quotation from pre-approved vendor                  │
├──────────────────────────────────────────────────────────┤
│                            [Apply now →] [Save for later]│
└──────────────────────────────────────────────────────────┘
```

### Rules
- Collapsed state must fit comfortably in a card stack on 375px — max 80px height collapsed
- Required documents checklist: pre-tick (☑) documents already uploaded via Document Agent; leave unticked (☐) what's still needed
- Eligibility gaps must be shown inline with a specific figure ("your profile: S$18K"), not generic ("you don't qualify")
- "Apply now" opens EnterpriseSG (or relevant authority) in a new tab; fires `application.submitted` event on tap
- "Save for later" adds to a saved instruments list (bookmarking — P2 feature; show as greyed-out with "Coming soon" at launch)

### Ranking Logic (visible to PM/engineering, not users)
Cards rendered in order of: `eligibility_confidence_score × estimated_value_midpoint`, descending. `unlikely` cards rendered last and visually separated from `likely` + `possible` cards.

---

## FI Rate Comparison Card

**Purpose:** Displays a single financial institution's green loan offering in the Loan Routing screen. Mobile: card stack. Desktop: table row.

### Anatomy — Mobile Card

```
┌──────────────────────────────────────────────────────┐
│  OCBC Green Business Banking                         │
│  Indicative rate: 3.1% p.a.          [Apply →]      │
│  Loan amount: up to S$3M                             │
│  Tenor: up to 7 years                                │
│                                                      │
│  Save 1.1% p.a. vs. your current rate   ← gain text │
└──────────────────────────────────────────────────────┘
```

### Anatomy — "Current Rate" Comparison Row (desktop table / mobile card)

```
┌──────────────────────────────────────────────────────┐
│  ⚠ Your current conventional loan                    │  ← amber background
│  4.2% p.a.                                           │
│  This is what you're paying today                    │
└──────────────────────────────────────────────────────┘
```

### Rules
- Current rate row always rendered first and in `color-signal-caution-bg` — makes the delta unmissable
- Delta text ("Save 1.1% p.a.") rendered in `color-signal-gain` inside each FI card
- FI logo (if available) displayed at 24px height — if no logo, use FI initials in a neutral pill
- "Apply via Navigator" triggers consent modal — never directly routes without consent
- Rates must be labelled "Indicative — subject to credit assessment" in `type-body-small`
- Maximum 4 FI cards displayed; if more FIs onboard in future, add a "Show more" disclosure

---

## Document Upload Zone

**Purpose:** File upload interface for the Document Agent. Two instances per screen: utility bills zone + P&L zone.

### Anatomy — Idle

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│         [Upload icon]                                │
│         Drag and drop your utility bills here        │
│         or tap to select files                       │
│                                                      │
│         PDF, JPG, PNG — max 10MB per file            │
│         Last 6 months recommended                   │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### Anatomy — Files Loaded

```
┌──────────────────────────────────────────────────────┐
│  SP Group Bill — Oct 2025.pdf        ████████ 100% ✓ │
│  SP Group Bill — Nov 2025.pdf        ████████ 100% ✓ │
│  SP Group Bill — Dec 2025.pdf        ████░░░░  62% … │
│  Genco Bill — Jan 2026.pdf           ░░░░░░░░   0% ↻ │  ← retry on failed
│                                                      │
│                              [+ Add more files]      │
└──────────────────────────────────────────────────────┘
```

### States
| State | Visual |
|---|---|
| Idle | Dashed border `color-neutral-400`; upload icon centred |
| Drag-over | Dashed border thickens to 2px `color-signal-info`; background `color-signal-info-bg` |
| Uploading | Per-file linear progress bar; percentage shown |
| Upload complete | Green tick + filename; progress bar replaced by tick |
| Upload failed | Red X + filename + "Retry" link; identified by filename, not by index |
| File outside date range | Amber warning inline below filename: "This bill is from Oct 2024 — older than 6 months. It will be accepted but won't affect your baseline." |

### Rules
- Each file identified by name in all states — never "File 3 failed"
- Minimum tap target for the zone: full width, min 120px height on mobile
- Failed upload shows retry inline — no toast notifications for individual file failures
- "Outside date range" is a warning, not a block — always accept the file

---

## OCR Confidence Indicator

**Purpose:** Shows extraction confidence for each field parsed by the Document Agent. Appears on the document review screen post-analysis.

### Anatomy

```
Monthly consumption (kWh)
┌────────────────────────┐
│  12,450 kWh            │  ← auto-filled from OCR
└────────────────────────┘
✓ Verified — confidence 94%                 ← type-body-small, color-signal-gain

Billing period
┌────────────────────────┐
│  Nov 2025              │
└────────────────────────┘
⚠ Please verify — our reading may be inaccurate (confidence 71%)  ← amber
  [Edit this field]
```

### States

| State | Confidence | Indicator | Field behaviour |
|---|---|---|---|
| High confidence | ≥88% | Green tick + "Verified — confidence X%" | Read-only; edit icon available on hover/tap |
| Low confidence | <88% | Amber warning icon + "Please verify" | Pre-filled but editable; amber border on field |
| Manual override | Any | Blue pencil icon + "Manually entered" | Field background `color-signal-info-bg` |

### Rules
- All low-confidence fields surfaced in a single review screen — never paginated one-at-a-time
- Auto-save on field blur — no save button
- High-confidence fields are editable on tap (user may know something OCR doesn't) — no fields are locked
- Confidence percentage is shown to build trust, not to alarm; label carefully: "Verified — confidence 94%" not "Only 94% sure"

---

## Blurred Preview Gate

**Purpose:** Shows freemium users the existence and count of matched instruments without revealing details. The primary freemium conversion surface.

### Anatomy

```
┌──────────────────────────────────────────────────────┐
│  3 instruments found for your profile               │  ← exact count, bold
│                                                      │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  EEG Advanced Tier   [LIKELY] │  ← instrument name visible, value blurred
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  EFS-Green           [LIKELY] │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  SME SRP             [POSSIB] │
│                                                      │
│  ┌────────────────────────────────────────────────┐  │
│  │  Unlock your full Navigator — S$99/month      │  │  ← primary CTA button
│  └────────────────────────────────────────────────┘  │
│  See application links, required documents, and       │
│  your full eligibility details                        │
└──────────────────────────────────────────────────────┘
```

### Rules
- **Exact instrument count must be visible** ("3 instruments found") — not "Some instruments found", not a lock icon
- **Instrument category names must be visible** — users need to know *what* they're missing to make the upgrade decision
- **Eligibility badges must be visible** — "Likely" and "Possible" badges create urgency without requiring the user to subscribe blind
- **Financial values are blurred** — the thing locked behind the paywall is the *specific dollar amounts and application detail*, not the existence of the instruments
- Blur implementation: CSS `filter: blur(4px)` on the value columns only — not on the full card
- Never animate the blur away as a teaser — that is a dark pattern

---

## WACC Impact Panel

**Purpose:** Displays the borrowing cost comparison and 5-year saving from the WACC + Brown Discount model. Appears on the Navigator dashboard post-loan-match.

### Anatomy

```
┌──────────────────────────────────────────────────────┐
│  Capital Impact Summary                              │
│                                                      │
│  Current facility          OCBC Green Loan           │
│  4.2% p.a.                 3.1% p.a.                 │
│  (conventional)            (matched via Navigator)   │
│                                                      │
│  Annual saving             5-year saving             │
│  S$2,750                   S$13,750                  │  ← type-data, color-signal-gain
│                                                      │
│  On a S$250,000 loan over 5 years                    │  ← type-body-small
│  Indicative — subject to final credit terms          │
│                                                      │
│  [Export as PDF — Capital Impact Summary]            │
└──────────────────────────────────────────────────────┘
```

### States
- **Pending approval:** "Updating your model — OCBC approval pending confirmation." Shimmer on saving figures.
- **Approved:** Full figures shown; `capital.approval.confirmed` must be received before figures render
- **No loan matched yet:** Panel hidden — not shown as empty/zero

---

## Brown Discount Risk Card

**Purpose:** Communicates the balance sheet risk of uncertified assets and the prevention value of green certification. Companion to the WACC Impact Panel.

### Anatomy

```
┌──────────────────────────────────────────────────────┐
│  [cost variant]  Brown Discount Risk                 │
│                                                      │
│  Without green certification                         │
│  S$540,000 – S$720,000  ← type-data, color-signal-cost
│  estimated valuation gap by 2030                     │
│                                                      │
│  With green certification (EEG Advanced)             │
│  S$108,000 – S$144,000  ← type-data, color-signal-gain
│  reduced exposure — 80% risk prevention              │
│                                                      │
│  Based on: Manufacturing sector · Building age: 12 years │  ← type-body-small
│  Indicative estimate — v1 static lookup table.       │
│  Not a certified valuation.                          │
└──────────────────────────────────────────────────────┘
```

### Rules
- **Always show both states** — without certification (cost/red) and with certification (gain/green) side by side or stacked
- "Not a certified valuation" disclaimer is mandatory — in `type-body-small`, not hidden in a tooltip
- Lookup table version number displayed (same versioning approach as Calculator formula)

---

## Progress Stage Indicator

**Purpose:** Shows the user's position in the onboarding flow (Calculator → Document Agent → Grant Match → Loan Routing). Persistent at top of each stage screen.

### Anatomy

```
  ①  Calculator   ——   ②  Documents   ——   ③  Grants   ——   ④  Finance
  [complete]           [active]             [locked]          [locked]
```

### States

| Stage state | Visual |
|---|---|
| Complete | Filled circle (`color-signal-gain`), label in `color-neutral-700` |
| Active | Filled circle (`color-signal-info`), label bold `color-neutral-900` |
| Locked (not yet reached) | Outline circle (`color-neutral-400`), label `color-neutral-400` |

### Rules
- Visible on all stage-specific screens; hidden on landing page (Calculator is pre-funnel)
- Mobile: horizontal scroll on the indicator bar is acceptable; do not stack vertically
- "Locked" stages are visible (not hidden) — showing the full path reduces abandonment

---

## Consent Modal

**Purpose:** Explicit per-FI, per-application consent before sending the bank-ready dossier to a financial institution.

### Anatomy

```
┌──────────────────────────────────────────────────────┐
│  Share your profile with OCBC?                       │
│                                                      │
│  Navigator will share the following with             │
│  OCBC Green Business Banking:                        │
│                                                      │
│  ✓  Your ESG baseline (energy consumption, sector)   │
│  ✓  Your grant eligibility summary                   │
│  ✗  Your P&L (not shared without separate sign-off)  │
│                                                      │
│  OCBC will use this to process your green loan       │
│  application. This consent applies to this           │
│  application only.                                   │
│                                                      │
│  [Share profile with OCBC]   [Cancel]                │
└──────────────────────────────────────────────────────┘
```

### Rules
- FI must be named specifically — never "a partner bank"
- Explicitly list what IS shared and what IS NOT shared
- "This application only" — no blanket consent
- Primary button: "Share profile with [FI name]" — not generic "Confirm" or "Proceed"
- Consent record stored server-side with timestamp for audit

---

## Application Status Pill

**Purpose:** Compact status indicator for the "My applications" view. Shows the current state of each submitted application.

**Variants:** `sent` | `in-review` | `approved` | `declined` | `expired`

| Variant | Background | Text | Icon |
|---|---|---|---|
| `sent` | `color-signal-info-bg` | "Sent to [FI]" | Send |
| `in-review` | `color-signal-caution-bg` | "In review" | Clock |
| `approved` | `color-signal-gain-bg` | "Approved" | CheckCircle |
| `declined` | `color-signal-cost-bg` | "Not approved" | XCircle |
| `expired` | `color-neutral-100` | "Expired" | AlertCircle |

---

## Formula Version Footer

**Purpose:** Displays the version and last-updated date of the Calculator formula on the results screen. Builds trust and enables audit.

### Anatomy

```
Formula v1.0 · 2026-04-03 · Indicative estimate — not financial advice.
Grant estimates are not a guarantee of eligibility. Values based on sector averages and published coefficients.
```

**Branch B variant** (MyInfo-connected):
```
Formula v1.0 · 2026-04-03 · Based on your ACRA-verified company data.
Indicative estimate — not financial advice. Grant estimates are not a guarantee of eligibility.
```

**Style:** `type-mono`, `color-neutral-400`, aligned to bottom of results screen; max 2 lines

### Rules
- Always visible on every Calculator results screen (Branch A and B) — never in a tooltip or expandable
- Formula spec reference: `docs/specs/sme-capital-advantage-formula-spec-v1.0.md`
- Version number increments when any coefficient or logic changes — PM owns versioning; Engineering implements
- Both "not financial advice" and "not a grant guarantee" lines are mandatory — legal has approved this framing (confirm before Stage 1 launch)
- Branch B footer swaps "sector averages" for "ACRA-verified company data" — same version number, different source attribution

---

## Eligibility Gap Card

**Purpose:** Shown when a grant instrument's eligibility status is "Unlikely." Explains the specific gap and provides a pathway to close it.

### Anatomy

```
┌──────────────────────────────────────────────────────┐
│  [UNLIKELY badge]  EEG Advanced Tier                 │
│                                                      │
│  Not yet eligible — here's the gap                   │
│                                                      │
│  Minimum qualifying capex: S$100,000                 │
│  Your current capex:        S$18,000                 │
│  Gap:                       S$82,000                 │
│                                                      │
│  How to close the gap:                               │
│  • Bundle multiple equipment upgrades in one project │
│  • Consider phased capex over 2 years (EEG allows   │
│    cumulative project value)                         │
│                                                      │
│  [Set a reminder for next grant cycle]               │
└──────────────────────────────────────────────────────┘
```

### Rules
- Never show Eligibility Gap Cards before "Likely" and "Possible" cards in the ranked list
- Always show the specific figure the user falls short by — never generic "insufficient capex"
- "How to close the gap" — 2–3 actionable bullet points max; sourced from grant scheme rules, not invented
- "Set a reminder" CTA captures email or sends in-app notification for the next grant application cycle

---

## SEFR Alignment Badge

**Purpose:** Trust signal displayed on all Calculator results screens (Branch A and Branch B) confirming that the Navigator's emission factors are sourced from the Singapore Emission Factors Registry (SEFR) — the same data used by MNCs for Scope 3 reporting. This is a positioning differentiator, not a decorative element.

**Maps to:** FR-01 AC-06 (formula versioning + sourcing transparency); formula spec v1.1

**Priority:** P0 — appears on the primary conversion screen.

### Anatomy

```
┌──────────────────────────────────────────────────────┐
│  [shield-check icon]  SEFR-ALIGNED 2026              │  ← type-label, all-caps
│                       Singapore Emission Factors     │  ← type-body-small
│                       Registry                       │
└──────────────────────────────────────────────────────┘
```

**Tap/hover expands tooltip:**
```
┌──────────────────────────────────────────────────────────────────────┐
│  Our calculations use the 2026 Singapore Emission Factors Registry — │
│  the same data used by MNCs for Scope 3 reporting.                   │
│                                                                      │
│  Most generic calculators use global averages (EPA/DEFRA) that are   │
│  10–30% less accurate for Singapore's grid.                          │
└──────────────────────────────────────────────────────────────────────┘
```

### Token Specifications

| Property | Value | Rationale |
|---|---|---|
| Background | `color-neutral-0` (#FFFFFF) | Clean; reads as verified data, not marketing |
| Border | `1px solid color-neutral-400` (#8B90A0) | Subtle containment |
| Border-radius | `space-4` (4px) | Consistent with badge language |
| Icon | Lucide `shield-check`, 16px, stroke 1.5px | Verification / authority signal |
| Icon colour | `color-signal-info` (#2563EB) | Authority blue — same as interactive elements |
| Label text | `type-label` (11px, 600, all-caps): `SEFR-ALIGNED 2026` | `color-neutral-900` |
| Sub-label | `type-body-small` (12px, 400): `Singapore Emission Factors Registry` | `color-neutral-700` |
| Padding | `space-8` horizontal, `space-4` vertical | Tight — this is a badge, not a card |
| Tooltip elevation | `elevation-2` | Dropdown-level overlay |

> **Do not use:** Green colour for this badge — it must read as a data authority badge, not a sustainability brand mark. The `color-signal-info` blue already signals "verified" without evoking eco-marketing.

### Placement

| Context | Placement |
|---|---|
| Calculator results (mobile 375px) | Full-width row below the last output card, above the Formula Version Footer |
| Calculator results (desktop 1280px) | Left-aligned inline, same row as the Formula Version Footer |
| Branch B results | Same placement; Branch B badge variant includes: `SEFR-ALIGNED 2026 · ACRA-Verified` to layer both trust signals |

### States

| State | Visual |
|---|---|
| Default | Badge as above |
| Hover (desktop) | Cursor becomes `help`; tooltip appears with 150ms delay |
| Tap (mobile) | Tooltip appears as bottom sheet (elevation-3); dismisses on tap-outside |
| Formula version mismatch (stale cache) | Not shown — engineering must never serve results from a stale formula version |

### Rules
- Always shown on results screens — cannot be dismissed or hidden
- Year in label (`2026`) must match the current SEFR database year; update to `SEFR-ALIGNED 2027` when SEFR 2027 is adopted
- Tooltip copy is fixed — do not A/B test the SEFR tooltip
- On Branch A results: badge appears without ACRA qualifier — "SEFR-ALIGNED 2026" only
- On Branch B results: badge can optionally display "SEFR-ALIGNED 2026 · ACRA-Verified" as a compound trust signal (PM to decide before Stage 1 build)
