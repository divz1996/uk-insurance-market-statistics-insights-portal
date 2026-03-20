# UK Insurance Market Statistics & Insights Portal (SQL + Power BI + Excel + Python)

> Insurance market statistics, ABI-style subscriptions and helpdesk simulation
> **Tools:** SQL · Power BI · DAX · Power Query (M) · Excel · Python

---

## Project Overview

An end-to-end business intelligence project I built around **ABI-style insurance market statistics**, simulating the subscriptions, data flows and helpdesk queries typical of a real market statistics portal. I scoped this project around the operational needs of a **Head of Claims Operations** — covering claims volume, cost, SLA performance and regional/product trends — and deliver a full star schema data model, MI SQL views, and a two-page Power BI dashboard.

---

## ABI-Style Simulation Context

I modelled this project on the type of **market statistics portal** operated by the Association of British Insurers (ABI) and similar industry bodies. It simulates:

- **Subscriptions** — organisations subscribing to receive regular claims and market performance data feeds
- **Helpdesk queries** — internal and external stakeholders raising questions about data definitions, SLA metrics, and regional breakdowns
- **MI reporting cadence** — monthly and quarterly reporting cycles typical of a UK insurance market statistics function

The dataset and schema are designed to replicate the structure a Claims Operations team would use when consuming ABI-style statistics for performance benchmarking and regulatory insight.

---

## Business Questions Answered

- Which regions have the highest SLA breach rates and longest settlement times?
- What is the monthly trend in claim volume and total settlement cost?
- Which products are driving the most leakage?
- Where should resourcing and process improvements be focused?

---

## Data Architecture — Star Schema

| Table | Type | Description |
|---|---|---|
| `fact_claims` | Fact | Core claims records — amounts, settlement days, SLA flag, leakage |
| `dim_region` | Dimension | Regional breakdown |
| `dim_product` | Dimension | Insurance product types |
| `dim_claimtype` | Dimension | Nature/category of claim |
| `dim_date` | Dimension | Full date hierarchy (year, quarter, month) |

---

## SQL MI Views

| View | Purpose |
|---|---|
| `vw_Claims_KPI_By_Month_Region` | Monthly KPIs by region — volume, cost, SLA breach rate |
| `vw_Claims_By_Product` | Product-level claims performance and settlement analysis |
| `vw_Claims_SLA_Breach` | Deep-dive into breach drivers by region, product and claim type |

All views are defined in `data/abi_star_schema_and_mi_views.sql`.

---

## Repository Structure

uk-insurance-market-statistics-insights-portal/
|
+-- data/
| +-- cleaned_insurance_claims.csv # Raw cleaned source data
| +-- fact_claims.csv # Fact table
| +-- dim_region.csv # Dimension: Region
| +-- dim_product.csv # Dimension: Product
| +-- dim_claimtype.csv # Dimension: Claim Type
| +-- dim_date.csv # Dimension: Date
| +-- abi_star_schema_and_mi_views.sql # ABI-style star schema DDL + MI views
| +-- abi_claims_dashboard.pbix # Power BI source file
|
+-- reports/
| +-- abi_mi_report.xlsx # Excel MI report: KPI + Regional + Product + Monthly
| +-- abi_claims_dashboard.pdf # Power BI dashboard export (2 pages)
|
+-- abi_market_statistics_pipeline.py # Python data pipeline: cleaning, star schema build, GitHub push
+-- LICENSE

text

---

## Insights & Recommendations

All insights are derived from the dataset fields: `fraud_reported`,
`incident_severity`, `total_claim_amount`, `incident_type`, `policy_state`,
`policy_deductable`, `bodily_injuries`, and `police_report_available`.

---

### Insight 1 — Fraud Flags Are Concentrated in Specific Incident Types
A material proportion of claims carry a `fraud_reported = Y` flag. Analysis
shows this is not evenly distributed — certain incident types (particularly
theft and collision claims) account for a disproportionate share of flagged
cases. Fraudulent claims inflate total payout figures and skew average cost
metrics if not separated out.

**Recommendation:** Theft and collision claims with bodily injury involvement
should require police report confirmation (`police_report_available`) before
settlement is authorised. The business should route high-fraud-rate incident
types to an enhanced validation queue rather than standard processing.

---

### Insight 2 — Incident Severity is the Primary Driver of Claim Cost
Total Loss and Major Damage incidents carry significantly higher
`total_claim_amount` values than Minor or Trivial claims. The majority of total
payout is driven by a relatively small number of high-severity cases.

**Recommendation:** Reserving and handler capacity should be weighted toward
Total Loss and Major Damage cases. Routing these to specialist handlers at FNOL
will reduce settlement time and leakage on the claims that matter most to the
cost base.

---

### Insight 3 — Regional Claim Volume and Cost Are Uneven
`policy_state` (mapped to regions) shows clear variation in both claim volume
and average `total_claim_amount`. Some regions generate high volumes of
lower-cost claims; others show lower volume but significantly higher average
cost per claim.

---

### Insight 4 — Third-Party Claims Carry Higher Complexity
Claims mapped to third-party incident types show elevated `bodily_injuries` and
`number_of_vehicles_involved` values, contributing to greater settlement
complexity and higher average costs compared to single-vehicle incidents.

**Recommendation:** Third-party claims involving bodily injuries should be
escalated to specialist handlers on receipt to reduce settlement time and
control costs on the most complex cases.

---

### Insight 5 — Lower Deductible Policies Drive Higher Claim Frequency
Policies with a `policy_deductable` of 500 generate more frequent claims,
including a higher proportion of minor and trivial severity incidents. Higher
deductible policies (1000, 2000) show lower frequency but higher average cost
per claim.

---


## Tools & Technologies

| Tool | Usage |
|---|---|
| **SQL** | Star schema design, MI views, data transformation |
| **Power BI** | Two-page dashboard — KPI cards, trend charts, SLA analysis |
| **DAX** | Calculated measures for breach rate, leakage %, MoM trends |
| **Power Query (M)** | Data shaping and ETL within Power BI |
| **Excel** | MI report for operational stakeholders |
| **Python** | Data cleaning, star schema generation, GitHub automation |
| **Google Colab** | Cloud-based Python execution and direct GitHub push |

---

## Author

**Divyansh Dubey**  
MBA — University of Bath | Data & Claims Analytics  
[GitHub](https://github.com/divz1996) · [LinkedIn](https://www.linkedin.com/in/divyanshdubey96)
