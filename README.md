# UK Insurance Market Statistics & Insights Portal (SQL + Power BI + Excel + Python)
> Insurance market statistics, ABI-style subscriptions and helpdesk simulation
> **Tools:** SQL · Power BI · DAX · Power Query (M) · Excel · Python

---

## Project Overview

An end-to-end business intelligence project built around **ABI-style insurance market statistics**, simulating the subscriptions, data flows and helpdesk queries typical of a real market statistics portal. The project is scoped around the operational needs of a **Head of Claims Operations** — covering claims volume, cost, SLA performance and regional/product trends — and delivers a full star schema data model, MI SQL views, and a two-page Power BI dashboard.

---

## ABI-Style Simulation Context

This project is modelled on the type of **market statistics portal** operated by the Association of British Insurers (ABI) and similar industry bodies. It simulates:

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

All views are defined in `data/insurance_claims_schema.sql`.

---

## Repository Structure

```
uk-insurance-market-statistics-insights-portal/
|
+-- data/
|   +-- cleaned_insurance_claims.csv       # Raw cleaned source data
|   +-- fact_claims.csv                    # Fact table
|   +-- dim_region.csv                     # Dimension: Region
|   +-- dim_product.csv                    # Dimension: Product
|   +-- dim_claimtype.csv                  # Dimension: Claim Type
|   +-- dim_date.csv                       # Dimension: Date
|   +-- insurance_claims_schema.sql        # Star schema DDL + MI views
|
+-- README.md
+-- LICENSE
```

---

## Key Insights & Recommendations

- Identified **underperforming regions** with above-average SLA breach rates and longer average settlement days
- Highlighted **high-leakage products** contributing disproportionately to total claims cost
- Proposed targeted **process and resourcing changes** to reduce breach rates and improve settlement efficiency
- Dashboard designed for leadership consumption — KPI cards, trend lines, and SLA/leakage deep-dive page

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

**Divyansh Verma**  
MBA — University of Bath | Data & Claims Analytics  
[GitHub](https://github.com/divz1996) · [LinkedIn](https://www.linkedin.com/in/divyansh-verma96)
