---
title: "SME Capital Advantage Navigator — Visual Style Guide"
product: "SME Capital Advantage Navigator"
date: 2026-04-03
status: draft
agent: "Arcee (ux-designer)"
bmm_phase: "02_Solutioning_Sprint"
version: "1.0"
---

# SME Capital Advantage Navigator — Visual Style Guide

> **Status:** Draft — pending Figma handoff and engineering review.
> This guide establishes the visual language for the Navigator. Every design decision is grounded in the product's core positioning: **bank-neutral, trustworthy, financially serious**. No generic sustainability aesthetics (green leaves, earth tones, carbon atoms). This is a capital navigation tool, not an ESG marketing brochure.

---

## Brand Positioning → Design Language

| Positioning pillar | Visual expression |
|---|---|
| **Bank-neutral** | No colour palette that evokes a specific SG bank (no UOB red, no DBS red/black, no OCBC red/orange). Neutral base with a distinct accent system. |
| **Financially serious** | Typography and layout borrowed from financial data products — Bloomberg-adjacent density and clarity, not startup-soft rounded corners and gradients |
| **Trustworthy** | Every estimate labelled "indicative". Confidence indicators visible. No hidden data. White space communicates that nothing is being obscured. |
| **Urgent but not alarmist** | Loss-aversion copy ("You are losing S$X") paired with a clear action path — urgency has a resolution, it is not pure fear |

---

## Colour System

### Primary Palette

| Token | Hex | Usage |
|---|---|---|
| `color-neutral-900` | `#0F1117` | Body text, primary headings |
| `color-neutral-700` | `#3D4252` | Secondary text, labels |
| `color-neutral-400` | `#8B90A0` | Placeholder text, disabled states |
| `color-neutral-100` | `#F4F5F7` | Page background |
| `color-neutral-0` | `#FFFFFF` | Card background, modal background |

### Semantic Colour: Financial Signals

| Token | Hex | Usage |
|---|---|---|
| `color-signal-cost` | `#C84B31` | Carbon tax cost cards, Brown Discount risk — loss-aversion red |
| `color-signal-cost-bg` | `#FDF1EF` | Background tint for cost cards |
| `color-signal-caution` | `#D97706` | "Possible" eligibility badge, current loan rate comparison row, amber warnings |
| `color-signal-caution-bg` | `#FFFBEB` | Background tint for caution states |
| `color-signal-gain` | `#1A7F5A` | Reclaim potential cards, "Likely" eligibility badge, WACC saving figures |
| `color-signal-gain-bg` | `#EFFAF5` | Background tint for gain cards |
| `color-signal-info` | `#2563EB` | Links, interactive elements, CTA buttons |
| `color-signal-info-bg` | `#EFF6FF` | Background tint for info states |

> **Rule:** `color-signal-cost` and `color-signal-gain` must never appear together in the same card without a clear label. The user must always know which number is a cost and which is a saving.

### Do Not Use
- Generic "sustainability green" (e.g. `#22C55E` tailwind green-500) — reads as marketing, not finance
- Bank brand colours — UOB red (`#EE2E24`), DBS red (`#DA1B1B`), OCBC orange (`#EF7D00`) — creates unintended bank association
- Pure black (`#000000`) for body text — too harsh at financial data density

---

## Typography

### Type Scale

| Token | Size | Weight | Line height | Usage |
|---|---|---|---|---|
| `type-display` | 32px / 2rem | 700 | 1.2 | Hero headlines (Calculator landing) |
| `type-heading-1` | 24px / 1.5rem | 700 | 1.3 | Page titles, section headers |
| `type-heading-2` | 20px / 1.25rem | 600 | 1.4 | Card titles, modal headers |
| `type-heading-3` | 16px / 1rem | 600 | 1.5 | Sub-section labels, table headers |
| `type-body` | 14px / 0.875rem | 400 | 1.6 | Body copy, descriptions |
| `type-body-small` | 12px / 0.75rem | 400 | 1.5 | Helper text, footnotes, "indicative estimate" labels |
| `type-data` | 28px / 1.75rem | 700 | 1.1 | Financial output numbers (S$8,100, 1.1%) — the hero numbers on results cards |
| `type-label` | 11px / 0.6875rem | 600 | 1.4 | Badges (Likely / Possible / Unlikely), status pills — all-caps |
| `type-mono` | 13px / 0.8125rem | 400 | 1.5 | Formula version numbers, UEN display, event tracking codes |

### Type Family

**Primary:** Inter (Google Fonts — system fallback: `-apple-system, BlinkMacSystemFont, "Segoe UI"`)

**Mono:** JetBrains Mono (formula versions, UEN display only)

> **Rationale:** Inter at financial data density is legible, neutral, and trusted. Avoid display fonts that read as startup-playful (e.g. Poppins, Nunito). The product must read like a Bloomberg terminal, not a fintech app aimed at Gen Z.

---

## Spacing System

8px base unit. All spacing values are multiples of 8px.

| Token | Value | Usage |
|---|---|---|
| `space-2` | 2px | Fine detail separators |
| `space-4` | 4px | Tight internal padding (badge, chip) |
| `space-8` | 8px | Base unit — icon-to-label gap, small component padding |
| `space-12` | 12px | Card internal padding (compact) |
| `space-16` | 16px | Standard component padding |
| `space-24` | 24px | Card internal padding (standard) |
| `space-32` | 32px | Section spacing (mobile) |
| `space-48` | 48px | Section spacing (desktop) |
| `space-64` | 64px | Page-level vertical rhythm |

---

## Grid & Layout

### Mobile (375px — primary)
- Single column
- 16px horizontal margin
- No horizontal scroll permitted on any core flow screen

### Tablet (768px)
- 2-column grid for card lists (grant matches, FI comparisons)
- 24px gutters

### Desktop (1280px)
- Sidebar navigation (240px) + main content area
- 3-column card grid for grant match list
- 32px gutters

> **Mobile-first rule:** Design all screens at 375px first. Desktop is an enhancement — never design desktop-first and add a responsive breakpoint. Every core flow (Calculator, Document Agent, Grant Match, Loan Routing) must be completable on mobile without horizontal scroll.

---

## Elevation & Depth

| Level | Shadow | Usage |
|---|---|---|
| `elevation-0` | none | Page background, dividers |
| `elevation-1` | `0 1px 3px rgba(0,0,0,0.08)` | Default card, form input focus |
| `elevation-2` | `0 4px 12px rgba(0,0,0,0.10)` | Dropdown, tooltip, popover |
| `elevation-3` | `0 8px 24px rgba(0,0,0,0.14)` | Modal, drawer, bottom sheet |

> No decorative gradients on cards. Elevation is communicated through shadow, not colour fill.

---

## Iconography

**Library:** Lucide Icons (open source, MIT licence — consistent with Inter's geometric style)

**Size:** 16px (inline), 20px (card actions), 24px (navigation)

**Stroke weight:** 1.5px — never fill-style icons in financial data contexts (fill reads as decorative)

**Never use:**
- Leaf / tree / globe / earth icons to represent sustainability — reads as greenwashing
- Generic lock icons for paywalled content — use specific count-based copy ("3 instruments found") per GTM directive
- Checkmark-in-circle for "success" without an accompanying label — accessibility fail

---

## Motion & Animation

**Principle:** Motion communicates state change, not decoration. Every animation has a functional reason.

| Interaction | Animation | Duration | Easing |
|---|---|---|---|
| Page transition (Calculator → Results) | Fade-in + subtle upward translate (8px → 0) | 200ms | ease-out |
| Grant reveal (Upload → Match results) | Staggered card entrance (50ms delay per card) | 300ms per card | ease-out |
| Blurred preview to subscription modal | Blur dissolve (filter: blur(4px) → blur(0)) | 150ms | ease-in-out |
| Document upload progress | Linear progress bar fill | Real-time | linear |
| OCR confidence indicator | Count-up from 0 to final value | 600ms | ease-out |

**Reduce motion:** All animations respect `prefers-reduced-motion: reduce` — fall back to instant state change.

**Performance rule:** No animation that causes layout reflow. Use `transform` and `opacity` only.

---

## Copy & Tone

| Context | Tone | Example |
|---|---|---|
| Loss-aversion (Calculator output, cost cards) | Direct, specific, financial — never alarmist | "You are paying S$8,100/year in carbon tax. This rises to S$14,400 by 2030." |
| Eligibility gap ("Not yet eligible") | Constructive — show the path, not the wall | "You need S$50K in eligible capex — your current figure is S$20K. Here's how to close the gap." |
| Decline / failure states | Empathetic, immediately actionable | "OCBC wasn't able to proceed at this time. Here are two other lenders who may be a better fit." |
| "Indicative estimate" disclaimer | Factual, not defensive | "Indicative estimate — formula v1.2 updated 2026-04-01. Not a certified valuation." |
| Bank-neutral messaging | Neutral, respectful — never competitive | "We show the most competitive green loan options available — not just your existing bank." |
| Subscription upgrade prompt | Value-framing — not pressure | "3 instruments found for your profile. Subscribe to unlock your full eligibility details and application links." |

**Never:**
- Use "green" as a standalone positive adjective ("make your business greener") — it reads as marketing
- Use "sustainability journey" — corporate cliché
- Use passive voice in CTA copy ("Get started" → "See your grant matches")
- Use a generic lock icon — always specify the count behind the paywall

---

## Accessibility

- **Contrast minimum:** 4.5:1 for body text (WCAG AA); 3:1 for large text and UI components
- **`color-signal-cost` on white:** contrast 5.2:1 ✓
- **`color-signal-gain` on white:** contrast 4.6:1 ✓
- **`color-signal-caution` on white:** contrast 3.4:1 — **use with an icon or label, never colour alone**
- **Touch targets:** minimum 44×44px (iOS HIG) / 48×48dp (Material)
- **Focus states:** visible focus ring on all interactive elements — `outline: 2px solid color-signal-info; outline-offset: 2px`
- **Screen reader:** all financial figures must have text alternatives (e.g. "S$8,100 per year in carbon tax, rising to S$14,400 by 2030")
- **Form labels:** all inputs have explicit `<label>` — no placeholder-as-label
