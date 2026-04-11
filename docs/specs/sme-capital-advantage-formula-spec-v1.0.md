---
title: "SME Capital Advantage Navigator — Green Alpha Calculator Formula Specification"
version: "1.1"
status: approved
date: 2026-04-03
updated: 2026-04-03
owner: "Product Manager"
reviewed_by: []
next_review: "2026-07-01"
sefr_aligned: true
sefr_version: "2026"
prd_reference: "FR-01 AC-06, FR-09 AC-15"
component_reference: "Formula Version Footer — v1.1 / 2026-04-03"
---

# Green Alpha Calculator — Formula Specification v1.1

> **Versioning rule:** Any change to a coefficient, lookup table value, or calculation logic requires a version increment (v1.0 → v1.1 → v2.0 etc.) and a corresponding update to the Formula Version Footer displayed on every Calculator results screen. Formula changes must be documented in the changelog below. The formula is deterministic: identical inputs must always produce identical outputs for the same formula version.

---

## Changelog

| Version | Date | Change | Author |
|---|---|---|---|
| 1.0 | 2026-04-03 | Initial specification — all three formulae defined | PM |
| 1.1 | 2026-04-03 | **SEFR alignment:** Grid Emission Factor updated from 0.4085 to 0.3952 kgCO₂e/kWh (SEFR 2026 Database). Business Travel (Regional) factor added to SEFR register (0.14 kg/km). Commercial Water factor added to SEFR register (0.42 kg/m³). Water and Business Travel factors documented but not yet in formula scope. All Formula 1 worked examples and output copy updated. SEFR-Aligned seal introduced. | PM |

---

## Inputs — Required vs. Derived

The Calculator collects a minimal set of direct inputs. Several formula inputs are **derived** (estimated from other inputs or from default coefficients) because collecting them directly would add friction. Engineering must implement derived inputs exactly as specified — they may not substitute alternative derivation methods without a version increment.

| Input | Type | Branch A | Branch B (MyInfo) | Source |
|---|---|---|---|---|
| Annual Electricity Spend (S$) | Direct — manual | ✓ | ✓ | User-entered |
| Current Loan Interest Rate (%) | Direct — manual | ✓ | Estimated (see §3A) | User-entered / paid-up capital bracket |
| Export Markets | Direct — manual | ✓ | ✓ | User-entered (multi-select) |
| Sector / SSIC Code | Derived (Branch A) / Direct (Branch B) | Default: all-sector average | ACRA via MyInfo | Sector dropdown (A) / MyInfo SSIC (B) |
| Company Revenue (S$) | Derived (Branch A) / Direct (Branch B) | Estimated from electricity spend (see §3A) | ACRA via MyInfo | Sector lookup (A) / MyInfo Financial Highlights (B) |
| Loan Principal (S$) | Derived — both branches | Estimated from revenue × sector leverage ratio (see §3A) | Estimated from revenue × sector leverage ratio | Sector lookup |
| Asset Valuation (S$) | Derived — both branches | Estimated from revenue × sector asset multiplier (see §2) | Estimated from revenue × sector asset multiplier | Sector lookup |
| Building Age Bracket | Derived — both branches | Default: Pre-2010 (conservative) — shown as assumption to user | Default: Pre-2010 (conservative) | Assumption |

> **Design note:** Derived inputs must be displayed to the user in the results screen as explicit assumptions (e.g. "We've assumed a Pre-2010 asset — adjust this for a more accurate Brown Discount estimate"). This is required for the "indicative estimate" framing and builds trust through transparency.

---

## Formula 1 — Carbon Tax Liability (Hidden OpEx)

**What it measures:** The carbon cost an SME is implicitly paying through electricity bills, passed through from power generators who bear the carbon tax. Framed as a "reclaimable hidden loss."

**Version:** 1.1
**Source:** SEFR 2026 Database (Singapore Emission Factors Registry); NEA Carbon Tax Schedule; SP Group Commercial/Industrial Tariff 2026

### Logic

$$\text{Liability (S\$)} = \frac{\text{Annual Electricity Spend (S\$)}}{\text{Average Tariff (S\$/kWh)}} \times \text{GEF (kgCO}_2\text{e/kWh)} \times \frac{\text{Carbon Tax Rate (S\$/tCO}_2\text{e)}}{1000}$$

The `/1000` converts kg to tonnes.

### Coefficients

| Coefficient | Value | Source | Review Date |
|---|---|---|---|
| Average Tariff | S$0.3245/kWh | Estimated 2026 commercial/industrial SME average — SP Group tier blended rate | Jul 2026 |
| Grid Emission Factor (GEF) | **0.3952 kgCO₂e/kWh** | **SEFR 2026 Database** — replaces EMA 2025 estimate of 0.4085. Reflects actual 2026 grid mix. | Upon SEFR 2027 publication |
| Carbon Tax Rate — 2025 | S$25/tCO₂e | NEA Carbon Pricing Act | Fixed (historical) |
| Carbon Tax Rate — 2026 | S$45/tCO₂e | NEA Carbon Pricing Act (current) | Fixed until NEA amendment |
| Carbon Tax Rate — 2030 (projected) | S$80/tCO₂e | NEA Carbon Pricing Act schedule | Fixed until NEA amendment |

### Multi-Year Output (2025 / 2026 / 2030)

The Calculator **must output all three years** on the results screen. This is the loss-aversion engine — the step-change from S$25 to S$45 (80% increase) is the urgency trigger, and the S$80 projection is the strategic hook.

$$\text{Liability}_{2025} = \frac{\text{Spend}}{0.3245} \times 0.3952 \times \frac{25}{1000}$$

$$\text{Liability}_{2026} = \frac{\text{Spend}}{0.3245} \times 0.3952 \times \frac{45}{1000}$$

$$\text{Liability}_{2030} = \frac{\text{Spend}}{0.3245} \times 0.3952 \times \frac{80}{1000}$$

Simplifying the constant factor (GEF / tariff / 1000):

$$k = \frac{0.3952}{0.3245 \times 1000} = 0.001218$$

| Year | Multiplier on Electricity Spend |
|---|---|
| 2025 (last year) | `spend × 0.001218 × 25` = spend × 0.030450 |
| 2026 (current) | `spend × 0.001218 × 45` = spend × 0.054810 |
| 2030 (projected) | `spend × 0.001218 × 80` = spend × 0.097440 |

### Worked Example

SME annual electricity spend: **S$180,000**

| Year | Calculation | Result |
|---|---|---|
| 2025 | 180,000 / 0.3245 × 0.3952 × 25/1000 | **S$5,480** |
| 2026 | 180,000 / 0.3245 × 0.3952 × 45/1000 | **S$9,865** |
| 2030 | 180,000 / 0.3245 × 0.3952 × 80/1000 | **S$17,537** |

### Output Copy Template

> "In 2025, your electricity bill included an estimated **S$5,480** in hidden carbon tax.
> In 2026, that rose to **S$9,865** — an 80% increase.
> By 2030, at the legislated rate, you will be paying **S$17,537/year** unless you act."

---

## Formula 2 — Brown Discount Risk

**What it measures:** The estimated erosion in asset valuation that an SME's property or equipment faces if it lacks green certification by 2030. Modelled as a percentage discount applied to estimated asset valuation.

**Version:** 1.0
**Source:** Savills Singapore 2026 market data; sector transition cost analysis

### Logic

$$\text{Brown Discount Risk (S\$)} = \text{Asset Valuation (S\$)} \times \text{Discount Factor (\%)}$$

### Step 1 — Derive Asset Valuation

Asset Valuation is not directly collected. Derived as:

$$\text{Asset Valuation (S\$)} = \text{Revenue (S\$)} \times \text{Sector Asset Multiplier}$$

**Sector Asset Multipliers (v1.0):**

| Sector | Asset Multiplier | Rationale |
|---|---|---|
| Manufacturing / Industrial | 2.5× revenue | High fixed-asset intensity; machinery, factory premises |
| F&B / Food Services | 1.2× revenue | Lower fixed assets; leasehold premises dominant |
| Commercial Real Estate | 4.0× revenue | Asset-heavy; property is the primary asset |
| Logistics / Warehousing | 2.0× revenue | Fleet + premises |
| All-sector default (Branch A no sector) | 2.0× revenue | Conservative mid-range assumption |

> **Engineering note:** These multipliers are internal calculation inputs. Do not surface them directly in the UI. The output shown to users is the estimated asset valuation range (with ±20% band) and the resulting Brown Discount risk — not the multiplier itself.

**Revenue Derivation (Branch A only):**

For Branch A users who don't provide revenue, revenue is estimated from electricity spend using a sector-average revenue-per-kWh coefficient:

$$\text{Revenue (S\$)} \approx \text{Electricity Spend (S\$)} \times \text{Revenue-to-Spend Ratio}$$

| Sector | Revenue-to-Spend Ratio | Basis |
|---|---|---|
| Manufacturing | 12× | Energy-intensive; lower revenue per electricity dollar |
| F&B | 20× | Energy less dominant in revenue model |
| Commercial Real Estate | 8× | Energy-heavy relative to revenue |
| Logistics | 15× | Mid-range |
| All-sector default | 13× | Conservative average |

*Example: S$180,000 electricity spend × 13 = S$2,340,000 estimated revenue. Manufacturing: × 12 = S$2,160,000.*

### Step 2 — Apply Discount Factor

**Lookup Table — Discount Factor (%):**

| Building Age | No Certification (Brown) | Basic / Gold | Platinum / SLE |
|---|---|---|---|
| Pre-2010 | 15% – 30% | 5% – 10% | 0% (Baseline) |
| Post-2010 | 8% – 15% | 2% – 5% | 0% (Baseline) |

**Sector Weighting:** Manufacturing / Industrial assets take the **upper end** of the Brown range (+5% additive to midpoint).

**Building Age Default:** Pre-2010 (conservative) — assumed for all Branch A users. Branch B: same default. In both branches, the building age assumption is displayed to the user explicitly as an editable assumption.

### Step 3 — Calculate Risk Range

For Branch A (no specific certification data), assume "No Certification (Brown)" state (since the user is exploring the platform — they likely have no certification yet).

Output as a **range** using the floor and ceiling of the discount band:

$$\text{Risk Low} = \text{Asset Valuation} \times \text{Discount\%}_{low}$$
$$\text{Risk High} = \text{Asset Valuation} \times \text{Discount\%}_{high}$$

### Worked Example

SME: Manufacturing, S$180,000 electricity spend, Branch A (no MyInfo)

1. Revenue estimate: S$180,000 × 12 = **S$2,160,000**
2. Asset valuation: S$2,160,000 × 2.5 = **S$5,400,000**
3. Discount factor (Pre-2010, No Certification, Manufacturing upper-end): 20% – 35% (15%–30% + 5% sector premium)
4. Risk range: S$5,400,000 × 20% = **S$1,080,000** to S$5,400,000 × 35% = **S$1,890,000**

Branch B (MyInfo, revenue S$2,400,000): S$2,400,000 × 2.5 = S$6,000,000 → Risk: **S$1,200,000 – S$2,100,000** (narrower band, revenue-specific)

### Output Copy Template

> "Without green certification, your assets face an estimated **S$1.08M – S$1.89M** valuation erosion by 2030.
> This is based on your sector (Manufacturing) and assumed Pre-2010 asset age. [Adjust assumption]
> With EEG Advanced Tier certification, this risk drops by up to 80%."

---

## Formula 3 — Green Finance Reclaim (Green Alpha)

**What it measures:** The total annual and long-term capital value unlocked by moving from a "Brown" to a "Green" financing position — combining interest savings from green loan rates and estimated grant value.

**Version:** 1.0

$$\text{Green Alpha (S\$)} = \text{Annual Interest Savings} + \text{Estimated Grant Value (annualised)}$$

---

### 3A — Annual Interest Savings

$$\text{Annual Interest Savings} = \text{Loan Principal (S\$)} \times (\text{Current Rate\%} - \text{Green Rate\%})$$

**Green Rate Coefficients (indicative, 2026):**

| FI | Green Loan Rate | Source |
|---|---|---|
| OCBC Green Loan | 3.1% p.a. | Indicative — OCBC Green Business Banking 2026 |
| Maybank Green Financing | 3.3% p.a. | Indicative — Maybank SME Green 2026 |
| Hong Leong Finance Green | 3.4% p.a. | Indicative — Hong Leong 2026 |
| **Calculator default (range)** | **3.1% – 3.4%** | Best-to-market range for display |

> **Rate disclaimer:** All rates are indicative and subject to credit assessment. Must be labelled "Indicative rate — subject to FI credit assessment" on every screen where rates are shown.

**Loan Principal Derivation:**

Loan Principal is not directly collected. Derived as:

| Branch | Method |
|---|---|
| Branch A | `Revenue × Sector Loan-to-Revenue Ratio` (see table below) |
| Branch B (MyInfo) | `Paid-up Capital × 2` (common SME green loan sizing convention; upper bound: S$3M) |

**Sector Loan-to-Revenue Ratio (Branch A default):**

| Sector | Loan-to-Revenue Ratio | Rationale |
|---|---|---|
| Manufacturing | 0.20 | Capex-heavy; green loans tied to equipment upgrade |
| F&B | 0.10 | Smaller capex; shorter loan terms |
| Commercial Real Estate | 0.30 | Green retrofit loans are large relative to revenue |
| Logistics | 0.15 | Fleet electrification loans |
| All-sector default | 0.15 | Conservative |

*Example: Revenue S$2,340,000 × 0.15 = S$351,000 estimated loan principal.*

**Current Rate (Branch B — if not entered):**

Estimated from paid-up capital bracket:

| Paid-up Capital | Estimated Current Rate |
|---|---|
| < S$100K | 5.5% p.a. |
| S$100K – S$500K | 4.8% p.a. |
| S$500K – S$2M | 4.2% p.a. |
| > S$2M | 3.8% p.a. |

Label displayed: *"Estimated from your paid-up capital — adjust if you know your exact rate."*

**Worked Example:**

SME: S$180,000 electricity spend, 4.2% current rate, Branch A

1. Revenue estimate: S$2,340,000 (all-sector default)
2. Loan principal: S$2,340,000 × 0.15 = **S$351,000**
3. Interest savings: S$351,000 × (4.2% – 3.1%) = S$351,000 × 1.1% = **S$3,861/year** (at OCBC best rate)
4. Interest savings range: S$3,861 (OCBC 3.1%) to S$3,158 (Hong Leong 3.4%)

---

### 3B — Estimated Grant Value

$$\text{Estimated Grant Value} = \min(\text{70\% of Qualifying Capex}, \text{Tier Cap})$$

**EEG Tier Selection Logic:**

| Condition | Tier | Grant Cap |
|---|---|---|
| Annual electricity spend > S$100,000 | **Advanced Tier** | S$350,000 |
| Annual electricity spend ≤ S$100,000 | **Base Tier** | S$30,000 |

**Qualifying Capex Derivation:**

Qualifying capex is not collected. Estimated as:

$$\text{Qualifying Capex} \approx \text{Loan Principal} \times 0.8$$

*(80% of loan principal assumed to be spent on eligible capex — conservative estimate. Remaining 20% covers soft costs, working capital, etc.)*

$$\text{Estimated Grant Value} = \min(0.7 \times \text{Qualifying Capex}, \text{Tier Cap})$$

**Worked Example:**

1. Loan principal (from above): S$351,000
2. Qualifying capex: S$351,000 × 0.8 = **S$280,800**
3. EEG tier: electricity spend S$180,000 > S$100,000 → **Advanced Tier**, cap S$350,000
4. Grant estimate: 70% × S$280,800 = S$196,560 → capped at S$350,000 → **S$196,560**

For Branch A, output as a **range**: Grant estimate ± 30% band (reflecting capex estimation uncertainty)
→ S$137,592 – S$255,528

---

### 3C — Total Green Alpha

$$\text{Green Alpha} = \text{Annual Interest Savings} + \text{Grant Value}$$

For the Calculator, grant value is shown as a one-time capital unlock, not annualised. Interest savings are shown annually and as a 5-year cumulative figure.

**Output structure:**

| Component | Value (example) | Label |
|---|---|---|
| Annual interest saving | S$3,158 – S$3,861/year | "Lower borrowing cost via green loan" |
| 5-year interest saving | S$15,790 – S$19,305 | "Over 5 years" |
| Estimated grant value | S$137,592 – S$255,528 | "One-time capital available via EEG" |
| **Total Green Alpha** | **S$153,382 – S$274,833** | "Capital you could unlock" |

**Output Copy Template:**

> "By switching to a green loan and applying for your eligible grants, you could unlock an estimated **S$153,000 – S$275,000** — including up to **S$256,000 in grants** and **S$19,000 in interest savings over 5 years**.
> This is your Green Alpha."

---

## Branch A vs Branch B — Output Precision Comparison

| Output | Branch A (sector averages) | Branch B (ACRA-verified) |
|---|---|---|
| Carbon Tax Liability | ±0% (formula is exact given inputs) | ±0% (same formula, ACRA revenue not used in F1) |
| Brown Discount Risk | ±30–40% (revenue estimated from spend) | ±15–20% (revenue from ACRA; asset multiplier still estimated) |
| Green Alpha — Interest Savings | ±35% (revenue and loan principal estimated) | ±15% (paid-up capital from ACRA; current rate from bracket if not entered) |
| Green Alpha — Grant Value | ±30% (capex estimated from loan principal) | ±20% (capex still estimated; EEG eligibility improved by SSIC + revenue) |

**UI labelling rule:**
- Branch A outputs: *"Estimated from sector averages — wide range. Connect MyInfo Business for your exact figures."*
- Branch B outputs: *"Based on your ACRA-verified company data — [date]."*

---

## SEFR Alignment

The Navigator's emission factor coefficients are sourced from the **Singapore Emission Factors Registry (SEFR)** — the authoritative national database maintained by the Singapore government for Scope 1, 2, and 3 emissions quantification. SEFR is published annually and is the reference used by MNCs filing GHG inventories and Scope 3 supply chain disclosures in Singapore.

### Why SEFR Matters for SMEs

Most generic online calculators and AI tools use global emission factor averages (US EPA, UK DEFRA, or IPCC defaults). These are off by 10–30% for Singapore's grid, which has a distinct fuel mix (natural gas dominant, LNG imports, and solar integration growing faster than global averages). Using SEFR produces materially more accurate results for Singapore-based electricity consumers — and makes the Navigator's output defensible in Scope 3 reporting conversations with MNC buyers and banks.

### SEFR 2026 — Emission Factors Used in Navigator v1.1

| Emission Factor | SEFR 2026 Value | Navigator v1.0 (old) | Status | Formula Scope |
|---|---|---|---|---|
| Purchased Electricity (Grid) | **0.3952 kgCO₂e/kWh** | 0.4085 kgCO₂e/kWh | **Updated in v1.1** | Formula 1 — Carbon Tax Liability |
| Commercial Water | 0.42 kgCO₂e/m³ | 0.40 kgCO₂e/m³ | Documented — not yet in formula | Reserved for Phase 2 (water footprint module) |
| Business Travel (Regional aviation) | 0.14 kgCO₂e/km | 0.12 kgCO₂e/km | Documented — not yet in formula | Reserved for Phase 2 (travel emissions module) |

> **Note on water:** SEFR 2026 shows water becoming more carbon-intensive (0.40 → 0.42 kgCO₂e/m³) due to increased desalination capacity. This trend is expected to continue. Flag for Phase 2 roadmap.

> **Note on business travel:** The regional aviation factor increase (0.12 → 0.14) reflects the 2026 regional aviation fuel and SAF mix. Not in scope for the Carbon Tax Liability formula (which models electricity-linked carbon cost only) but relevant if the Navigator expands to full Scope 1+2+3 baseline in Phase 2.

### SEFR-Aligned Seal — Display Specification

All Calculator results screens (Branch A and Branch B) must display the SEFR-Aligned seal. This is a trust signal and positioning differentiator — not a decorative element.

**Copy (exact):**
- **Badge label:** `SEFR-ALIGNED 2026`
- **Sub-label:** `Singapore Emission Factors Registry`
- **Tooltip / tap-to-expand copy:** *"Our calculations use the 2026 Singapore Emission Factors Registry — the same data used by MNCs for Scope 3 reporting. Most generic calculators use global averages that are 10–30% less accurate for Singapore."*

**Visual spec:** See `sme-capital-advantage-component-library.md` → SEFR Alignment Badge.

**Placement:** Bottom of the results card stack, above the Formula Version Footer. On mobile: full-width row. On desktop: inline-left aligned below the last output card.

**Review cadence:** SEFR is published annually (typically Q1). When SEFR 2027 is published, run a coefficient comparison. If any in-formula factor changes by >2%, trigger a formula version increment and update the seal year.

---

## Coefficient Review Schedule

| Coefficient | Current Value | Source | Review Trigger | Owner |
|---|---|---|---|---|
| Average Tariff (S$/kWh) | S$0.3245 | SP Group | SP Group tariff revision (quarterly) | Engineering + PM |
| Grid Emission Factor (GEF) | **0.3952 kgCO₂e/kWh** | **SEFR 2026** | SEFR annual publication (Q1) — compare to SEFR 2027 when available | Engineering + PM |
| Commercial Water Factor | 0.42 kgCO₂e/m³ | SEFR 2026 | SEFR annual publication — monitor trend (desalination impact) | PM |
| Business Travel Factor (Regional) | 0.14 kgCO₂e/km | SEFR 2026 | SEFR annual publication | PM |
| Carbon Tax Rate — 2026 | S$45/tCO₂e | NEA | NEA Carbon Pricing Act amendment | PM |
| Carbon Tax Rate — 2030 | S$80/tCO₂e | NEA | NEA Carbon Pricing Act amendment | PM |
| Green Loan Rates (OCBC, Maybank, Hong Leong) | 3.1% – 3.4% | FI partners | FI partner rate updates (monthly check) | BD + PM |
| Sector Asset Multipliers | 2.0× – 4.0× | Savills SG | Annual review against Savills/CBRE SG data | PM |
| Sector Loan-to-Revenue Ratios | 0.10 – 0.30 | Internal | Annual review | PM |
| Sector Revenue-to-Spend Ratios | 8× – 20× | Internal | Annual review | PM |
| EEG Grant Caps | S$30K (Base) / S$350K (Advanced) | EnterpriseSG | EnterpriseSG scheme revision | PM |

---

## Open Engineering Questions

| # | Question | Impact | Required By |
|---|---|---|---|
| EQ-01 | Building Age is defaulted to Pre-2010 (conservative). Should the Calculator optionally collect building age as a 4th Branch A input, or always default and let the user adjust the assumption on the results screen? | Affects Brown Discount precision | Before Stage 1 build |
| EQ-02 | For Branch B users where ACRA Financial Highlights are unavailable (recently incorporated), which formula paths fall back to Branch A logic? Revenue-to-spend ratio? Must be defined before Branch B goes to QA. | Affects Branch B fallback completeness | Before Branch B build |
| EQ-03 | Grant value annualisation: the Calculator shows grant value as a one-time figure. Should the 5-year view amortise the grant over the loan tenor for comparability? | UX only — no formula change; but output copy needs PM decision | Before Stage 1 build |
| EQ-04 | Formula versioning implementation: how is the formula version stored and surfaced? Options: (a) hardcoded string in config, (b) database-driven with admin panel, (c) environment variable. Must be auditable. | Architecture decision | Before Stage 1 build |

---

## Compliance Notes

- All outputs must be accompanied by: *"Indicative estimate — formula v1.1 dated 2026-04-03. SEFR-Aligned 2026. Not financial advice. Values are estimates based on sector averages and SEFR-verified emission factors."*
- Formula is not a licensed financial product — it is a decision-support tool. Legal must confirm this framing is sufficient under MAS guidelines before Stage 1 launch.
- EEG grant estimates are directional — the platform does not guarantee eligibility. Copy must include: *"Grant eligibility is subject to EnterpriseSG assessment. This is not a grant approval."*
