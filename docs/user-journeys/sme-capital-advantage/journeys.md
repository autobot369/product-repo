---
title: "SME Capital Advantage Navigator — User Journey Reference"
product: "SME Capital Advantage Navigator"
date: 2026-04-03
status: approved
agent: "Arcee (ux-designer)"
bmm_phase: "02_Solutioning_Sprint"
version: "1.1"
changelog: "v1.1 — Journey 1 updated to two-branch architecture with MyInfo Business integration (Corppass OAuth)"
personas:
  - "Rachel — CFO / Finance Director, SG SME Manufacturing, 45 employees"
  - "Wei — Operations Manager, SG SME F&B, 28 employees"
journeys:
  - "J1: Green Alpha Calculator — Branch A (Quick Estimate) + Branch B (MyInfo Business)"
  - "J2: Document Agent → Grant Eligibility Match (Activation)"
  - "J3: Green Loan Routing → Bank-Ready Dossier → Success Fee (Revenue)"
myinfo_integration:
  api: "MyInfo Business API v2.0"
  spec: "https://public.cloud.myinfo.gov.sg/myinfobiz/myinfo-biz-specs-v2.0.html"
  auth: "Corppass OAuth 2.0"
  prd_reference: "FR-09"
---

# SME Capital Advantage Navigator — User Journey Reference

> **Source of truth:** Journeys are embedded inline into `tools/bmm/output/prds/final-prd.md` under `## Functional Requirements → ### User Journeys`. This file is the canonical standalone reference for sharing, reviewing, and onboarding designers and researchers.

---

## MyInfo Business Integration — Data Map

The MyInfo Business API (v2.0) is the most significant data integration in the Navigator. It eliminates the majority of manual onboarding friction and provides ACRA-verified data as the foundation for grant eligibility scoring.

| MyInfo Field | Source | Navigator Use | Available in Branch |
|---|---|---|---|
| UEN | ACRA | Entity identifier, UEN-gating | B (auto) |
| Entity Name | ACRA | Auto-populate company name | B (auto) |
| Entity Status | ACRA | Active check (must be "Live" for eligibility) | B (auto) |
| Entity Type / Company Type | ACRA | Grant filter (Pte Ltd vs. sole prop) | B (auto) |
| Registration Date | ACRA | Company age (some grants require ≥2 years) | B (auto) |
| Primary Activity (SSIC code) | ACRA | Sector classification — replaces sector dropdown | B (auto) |
| Registered Address | ACRA | Location eligibility | B (auto) |
| Paid-up Capital Amount | ACRA | SME threshold check, loan rate estimate | B (auto) |
| Company Revenue (latest year) | ACRA | Carbon tax liability, grant financial threshold | B (auto) |
| Company Profit/Loss Before Tax | ACRA | Loan eligibility indicator | B (auto) |
| Financial Period Start/End | ACRA | Ensures correct financial year used | B (auto) |
| Grants Type + Status + Amount | MTI | Deduplication + upgrade path surfacing | B (auto) |

**Fields still requiring manual input (both branches):**
- Annual electricity spend (kWh / S$) — not in any government dataset
- Export markets — not in MyInfo Business scope
- Current loan interest rate — estimated from paid-up capital bracket in Branch B; manual in Branch A

---

## Personas

### Rachel — CFO / Finance Director
- **Company:** Singapore SME, Manufacturing sector, 45 employees
- **Trigger:** Bank relationship manager requests ESG metrics for green loan renewal
- **Goal:** Access green finance at a lower rate; understand balance sheet impact of sustainability investment
- **Pain:** Bank portal (UOB SAGE) only shows UOB products; can't justify a sustainability consultant
- **Journeys:** J1 (both branches), J3 (Revenue)

### Wei — Operations Manager
- **Company:** Singapore SME, F&B sector, 28 employees
- **Trigger:** Rising electricity bill linked to carbon tax
- **Goal:** Find grants to fund energy efficiency upgrades without ESG expertise
- **Pain:** EnterpriseSG portal has no eligibility matching for F&B
- **Journeys:** J2 (Activation)

---

## Journey 1 — Acquisition: Green Alpha Calculator (Two Branches)

**Persona:** Rachel
**Funnel stage:** Front Funnel → Mid Funnel
**Trigger:** Bank ESG letter
**Entry point:** LinkedIn ad / SBF newsletter → Calculator landing page (no login)

```
Landing screen (both options visible above fold)
      │
      ├── Branch A: Quick Estimate (3 inputs) ──────→ Wide-range results → MyInfo CTA → Email → Signup
      │
      └── Branch B: Connect MyInfo Business (Corppass) → Auto-fill → 2 inputs → Exact results → Subscribe
```

---

### Branch A — Quick Estimate

**When:** Rachel wants fast numbers without Corppass; on mobile; or unfamiliar with the platform.

| Step | User action | System response | Design note |
|------|-------------|-----------------|-------------|
| A1 | Lands on Calculator; sees two options side by side | Quick Estimate (left) + "Connect MyInfo Business" with "More accurate" badge (right) | Never hide MyInfo option. Both visible above fold on 375px. |
| A2 | Taps Quick Estimate; 3-field form appears | Fields: (1) electricity spend (S$), (2) loan rate (%), (3) export markets | Sector inferred from sector-average tables — not asked. Reduces friction. |
| A3 | Enters S$180K spend, 4.2% rate, EU + Malaysia | Real-time validation | `type="number"` on mobile |
| A4 | Taps "Get my estimate" | Deterministic formula (≤2s) | Formula version in footer |
| A5 | Branch A results | **Wide bands** labelled "Estimated from sector averages": carbon tax S$6K–14K/yr, Brown Discount S$400K–900K, reclaim S$10K–35K/yr | Wide bands are honest. Never fake precision. |
| A6 | Below results: MyInfo upgrade prompt | "Get exact figures — connect MyInfo Business in 30 seconds." CTA + "Continue with estimate" secondary | This is the A→B conversion moment |
| A7 | Taps "Continue with estimate" | Optional email capture | Show results first, email after |
| A8 | Email entered; taps Continue | Email captured; transition to signup | Pre-fill email |
| A9 | Completes signup | Navigator Lite: blurred preview + persistent "Connect MyInfo Business" banner | MyInfo prompt persists inside Navigator Lite |
| A10 | Subscribes | Dashboard: Document Agent (2 paths — utility bills + optional MyInfo connect) | `subscription.activated` fired |

**Branch A → B conversion trigger:** The MyInfo CTA at A6 drops Rachel into Branch B step B1. Her email and Branch A results are preserved — she doesn't start over.

---

### Branch B — MyInfo Business (Corppass OAuth, exact values)

**When:** Rachel has Corppass ready; was nudged from Branch A result; or is desktop/office context.

| Step | User action | System response | Design note |
|------|-------------|-----------------|-------------|
| B1 | Taps "Connect MyInfo Business" (from landing or from Branch A results screen) | Corppass OAuth 2.0 redirect initiated | Standard Corppass flow; no Corppass credentials stored |
| B2 | Authenticates via Singpass / Corppass | Standard Singpass consent screen listing requested fields | Minimal scope — entity, financials, grants only |
| B3 | Redirected to Navigator | Auto-populated review card: "We found **[Entity Name]** (UEN: XXXXXXX). Retrieved from ACRA:" — table of ingested values with retrieval date | Show exactly what was retrieved and from where |
| B4 | Sees 2 remaining fields | Electricity spend (S$) + export markets | Loan rate pre-estimated from paid-up capital bracket with label "Estimated — you can adjust" |
| B5 | Enters electricity spend + export markets | Validation | Single screen, 2 fields only |
| B6 | Taps "Get my exact figures" | Deterministic formula with ACRA-verified inputs | MyInfo fields tagged "ACRA-verified" in calculation |
| B7 | Branch B results | **Narrow bands**, source-attributed: "Based on your revenue of S$2.4M (Manufacturing, SSIC 2511), you are paying **S$8,100/year** in carbon tax — rising to **S$14,400 by 2030**" | Revenue figure cited explicitly. Trust differentiator vs. Branch A. |
| B8 | Existing Grants insight card | "You have EEG Base Tier (Approved, S$45,000 — 2024). You may now qualify for **EEG Advanced Tier**." | Only possible with MyInfo MTI grant data. Major differentiator. |
| B9 | Email capture (optional) + signup | Pre-fill email from Corppass data if available | |
| B10 | Completes signup | Navigator Lite: blurred preview shows **deduplicated** count — "2 new instruments found" (EEG Base already claimed, excluded) | `myinfo.connected` flag set on profile |
| B11 | Subscribes | Dashboard: "Your financial data is connected via MyInfo — upload your utility bills to complete your baseline." | Document Agent: utility bills only. P&L not needed. `subscription.activated` fired. |

---

### Failure States (both branches)

| Trigger | Branch | Response |
|---------|--------|----------|
| Skips email | A | 7-day cookie restores results |
| Outlier input | A | Inline flag; non-blocking |
| Didn't subscribe | Both | 3-email nurture (Branch B emails reference ACRA revenue figure for personalisation) |
| Payment fails | Both | Specific error; session preserved |
| Corppass OAuth fails | B | Return to Calculator landing; Branch A pre-selected; banner: "MyInfo connection failed — try manual estimate below" |
| No Financial Highlights (recently incorporated) | B | "Financial data unavailable — enter your approximate revenue." 4-field fallback (Branch A + revenue). |
| UEN already registered | B | "This company already has a Navigator account. Sign in instead?" |

### Edge Cases
- **Branch A returning user:** Persistent "Upgrade your estimate" banner in Navigator Lite for up to 3 sessions
- **Multi-UEN director:** Corppass returns multiple UENs — company selector before proceeding
- **Stale ACRA data:** Retrieval date shown on all MyInfo values; user can override with manual entry
- **Corppass blocked by corporate firewall:** Fallback copy: "Try on mobile data or a different network" — Branch A always available

### Design Principles Check

| Principle | Branch A | Branch B |
|---|---|---|
| ≤3 taps to core value | ✓ Form → Results → Signup | ✓ OAuth → Auto-fill → Results |
| Mobile-first 375px | ✓ 3 inputs above fold | ✓ Singpass app handles Corppass mobile auth natively |
| Personalisation | Partial (sector-average) | ✓ Company-specific ACRA data; grant history deduplication |
| Quality bar | ✓ Wide bands are honest; no false precision | ✓ Source-attributed results feel like a financial briefing |

---

## Journey 2 — Activation: Document Agent → Grant Eligibility Match

**Persona:** Wei
**Funnel stage:** Mid Funnel
**Trigger:** Rising electricity bill; just subscribed post-Calculator
**Entry point:** Navigator dashboard → "Upload documents" onboarding card

### Happy Path

| Step | User action | System response | Design note |
|------|-------------|-----------------|-------------|
| 1 | Taps "Upload documents" | Two upload zones: utility bills + P&L | 48×48px tap targets; native file picker on mobile |
| 2 | Uploads 6 utility bills | Per-file progress + thumbnail previews | Identify failed files by name, not number |
| 3 | Uploads P&L | Confirmed | |
| 4 | Taps "Analyse my documents" | Staged progress labels: "Reading energy…", "Extracting financial…", "Cross-referencing grants…" | Trust-building micro-copy; not just a spinner |
| 5 | Analysis complete | Review screen: green ticks (≥88% confidence) + amber flags (<88%) with override | Auto-populate from OCR; flag for review |
| 6 | Corrects one flagged field | Baseline recalculates | Auto-save; no "Save" button |
| 7 | Taps "Confirm and get my grant matches" | Grant Eligibility Engine runs | Reveal transition — not a page reload |
| 8 | Match list renders | Ranked: EEG Base (Likely), EFS-Green (Possible), SME SRP (Likely) | Rank by confidence × value; "Unlikely" always last |
| 9 | Taps EEG Base Tier card | Expanded: eligibility checklist, required docs (pre-ticked if uploaded), application link | Pre-tick already-uploaded docs |
| 10 | Taps "Apply now" | EnterpriseSG opens in new tab; `application.submitted` fired | Event fires on tap, not on EnterpriseSG confirmation |

### Failure States

| Trigger | Response |
|---------|----------|
| >3 fields <88% confidence | Single review screen for all flagged fields |
| Unsupported bill format | Extract what's possible; manual entry for rest |
| P&L skipped | Partial match shown; P&L addable later |
| UEN already used free analysis | "Subscribe to run additional analyses" — framed as value |
| Grant database stale | Ops SLA; user-visible only if scheme officially closed |

### Edge Cases
- Bill >6 months old: flagged per file, non-blocking
- SME below grant threshold: gap shown ("You need S$50K capex — currently S$20K")
- Multi-user per UEN (Wei + accountant): company-scoped profile; invite as collaborator. **Wheeljack dependency: roles/permissions model required**

### Design Principles Check
| Principle | Status |
|---|---|
| ≤3 taps to core value | ✓ Upload → Analyse → Results |
| Mobile-first | Partial — multi-file upload needs "mobile quick entry" fallback |
| Personalisation | ✓ Profile-specific grant match |
| Quality bar | ✓ Upload → grant reveal requires deliberate transition design |

---

## Journey 3 — Revenue: Green Loan Routing → Bank-Ready Dossier → Success Fee

**Persona:** Rachel (returning — has grant matches; wants to finance retrofit)
**Funnel stage:** Bottom Funnel
**Trigger:** Grant match received; wants green loan without going back to existing bank
**Entry point:** Dashboard → "Finance your retrofit — compare green loans" CTA

### Happy Path

| Step | User action | System response | Design note |
|------|-------------|-----------------|-------------|
| 1 | Taps "Compare green loans" | Loan routing screen: "From banks who compete for your business" | Bank-neutral framing; challengers positioned as eager |
| 2 | Sees rate comparison | Cards: OCBC (3.1%), Maybank (3.3%), Hong Leong (3.4%) vs. current 4.2% (amber row at top) | Delta prominent: "Save up to 1.1% p.a." Amber = cost; green = saving |
| 3 | Taps "Apply via Navigator" for OCBC | Consent modal naming OCBC specifically | Per-FI, per-application consent. "Share profile" / "Cancel." |
| 4 | Confirms consent | Dossier sent to OCBC; "They'll be in touch within 3–5 business days" | `dossier.sent` fired; expectation set explicitly |
| 5 | OCBC approves | Dashboard: "OCBC green loan — Approved — S$250,000 at 3.1%" | `capital.approval.confirmed` fired; prominent on dashboard |
| 6 | WACC + Brown Discount auto-updates | WACC: "Save S$2,750/year. Over 5 years: S$13,750." Brown Discount: "Risk drops from S$720K to S$144K" | Auto-refresh on approval; Rachel re-enters nothing |
| 7 | Success fee invoiced | 0.5–1% of S$250,000 = S$1,250–2,500 | Method per OQ-03 |

### Failure States

| Trigger | Response |
|---------|----------|
| No FI partners live | Feature-flagged off; waitlist capture only |
| OCBC declines | "Two other lenders who may be a better fit" — immediately route to Maybank/Hong Leong |
| FI webhook unavailable | Proactive email on manual ops import of approval |
| Multi-FI applications | Per-FI consent; "My applications" tab shows all statuses |
| WACC model delayed | "Updating — OCBC approval pending confirmation" — never show stale data as current |

### Edge Cases
- Partial approval (S$200K of S$250K): WACC updated with approved amount, delta shown
- Offline deal finalised with OCBC directly: fee tracking broken — OQ-03 must address. **PM flag.**
- Rachel asks why UOB isn't listed: neutral copy — "We show the most competitive options available. Contact your UOB relationship manager for your existing facility." Never badmouth UOB.

### Design Principles Check
| Principle | Status |
|---|---|
| ≤3 taps to core value | ✓ Grant match → Loan comparison → Apply |
| Mobile-first | ✓ Card stack (not horizontal table) on mobile |
| Personalisation | ✓ Profile-specific indicative rates — not generic published rates |
| Quality bar | ✓ Rate delta (amber/green) must be unmistakable; no generic fintech blue-grey |

---

## Open Flags for Phase 03 (Architecture)

| Flag | Raised by | Required by |
|---|---|---|
| Session state API for 7-day Calculator cookie restore | Arcee | Phase 03 architecture |
| Multi-user per UEN roles/permissions model | Arcee | Phase 03 architecture |
| "My applications" dashboard tab (multi-FI status tracking) — gap in FR-05 | Arcee | Optimus Prime to confirm before Technical Readiness gate |
| Mobile quick entry fallback for Document Agent upload | Arcee | Phase 03 architecture |
