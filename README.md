# UK Insurance Market Statistics & Insights Portal

![SQL](https://img.shields.io/badge/SQL-Server-blue?logo=microsoftsqlserver) ![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-yellow?logo=powerbi) ![Excel](https://img.shields.io/badge/Excel-MI%20Report-green?logo=microsoftexcel) ![Python](https://img.shields.io/badge/Python-Analytics-blue?logo=python) ![License](https://img.shields.io/badge/License-MIT-lightgrey)

A end-to-end insurance analytics project simulating an **ABI-style** market statistics and management information (MI) portal. Built to answer the strategic questions a **Head of Claims Operations** asks about claims volume, cost, SLA performance, and regional/product trends — using SQL, Power BI, Excel, and Python.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Business Questions Addressed](#business-questions-addressed)
- [Data Architecture — Star Schema](#data-architecture--star-schema)
- [SQL MI Views](#sql-mi-views)
- [Power BI Dashboard](#power-bi-dashboard)
- [Excel MI Report](#excel-mi-report)
- [Key Insights & Recommendations](#key-insights--recommendations)
- [Tools & Technologies](#tools--technologies)
- [Repository Structure](#repository-structure)
- [How to Use](#how-to-use)
- [License](#license)

---

## Project Overview

This project simulates a UK insurance market intelligence portal, modelled after the kind of MI and analytics infrastructure used by major insurers and industry bodies (e.g., the ABI — Association of British Insurers). It covers the full analytics pipeline:

1. **Requirements gathering** — Defined key business questions for a Head of Claims Operations
2. **Data modelling** — Designed a star schema in SQL Server for scalable, repeatable reporting
3. **MI views** — Created reusable SQL views for KPIs, product performance, and SLA tracking
4. **Excel MI report** — Structured management information report for operational leaders
5. **Power BI dashboard** — Two-page interactive dashboard with KPI cards, trends, and SLA/leakage deep-dive
6. **Insights & recommendations** — Identified underperforming regions/products and proposed targeted process changes

---

## Business Questions Addressed

The following questions were defined to represent the analytical needs of a Head of Claims Operations:

| # | Business Question |
|---|-------------------|
| 1 | How many claims are we receiving per month, and is volume increasing? |
| 2 | What is the total and average cost of claims by product line and region? |
| 3 | What percentage of claims are breaching SLA thresholds, and where? |
| 4 | Which regions have the highest claim frequency and settlement costs? |
| 5 | Which product lines generate the most leakage and longest settlement times? |
| 6 | How does claims performance compare month-on-month and year-on-year? |
| 7 | Are there systemic SLA breach patterns linked to specific claim types or handlers? |

---

## Data Architecture -- Star Schema

A star schema was designed in SQL Server to support fast, flexible reporting across multiple dimensions.

```
                        +------------------+
                        |   dim_Date       |
                        +------------------+
                               |
+---------------+    +------------------+    +------------------+
|  dim_Region   |----|   fact_Claims    |----|  dim_Product     |
+---------------+    +------------------+    +------------------+
                               |
                        +------------------+
                        |  dim_ClaimType   |
                        +------------------+
```

### Fact Table
- **fact_Claims** — claim_id, date_key, region_key, product_key, claim_type_key, claim_amount, settlement_days, sla_breached (flag), handler_id

### Dimension Tables
- **dim_Date** — date_key, date, month, quarter, year, financial_year
- **dim_Region** — region_key, region_name, area, country
- **dim_Product** — product_key, product_name, product_line, coverage_type
- **dim_ClaimType** — claim_type_key, claim_type, severity_band

---

## SQL MI Views

Three repeatable MI views were created to power both the Excel report and the Power BI dashboard:

### `vw_Claims_KPI_By_Month_Region`
Aggregates claim volume, total cost, average settlement days, and SLA breach rate by month and region. Used for trend analysis and regional performance monitoring.

```sql
CREATE VIEW vw_Claims_KPI_By_Month_Region AS
SELECT
    d.year,
    d.month,
    r.region_name,
    COUNT(f.claim_id)                          AS total_claims,
    SUM(f.claim_amount)                        AS total_claim_cost,
    AVG(f.claim_amount)                        AS avg_claim_cost,
    AVG(f.settlement_days)                     AS avg_settlement_days,
    SUM(CAST(f.sla_breached AS INT))           AS sla_breach_count,
    ROUND(
        100.0 * SUM(CAST(f.sla_breached AS INT)) / COUNT(f.claim_id), 2
    )                                          AS sla_breach_pct
FROM fact_Claims f
JOIN dim_Date    d ON f.date_key    = d.date_key
JOIN dim_Region  r ON f.region_key  = r.region_key
GROUP BY d.year, d.month, r.region_name;
```

### `vw_Claims_By_Product`
Breaks down claims volume, cost, and SLA compliance by product line — enabling product-level profitability and leakage analysis.

```sql
CREATE VIEW vw_Claims_By_Product AS
SELECT
    p.product_name,
    p.product_line,
    COUNT(f.claim_id)                          AS total_claims,
    SUM(f.claim_amount)                        AS total_claim_cost,
    AVG(f.settlement_days)                     AS avg_settlement_days,
    ROUND(
        100.0 * SUM(CAST(f.sla_breached AS INT)) / COUNT(f.claim_id), 2
    )                                          AS sla_breach_pct
FROM fact_Claims f
JOIN dim_Product p ON f.product_key = p.product_key
GROUP BY p.product_name, p.product_line;
```

### `vw_Claims_SLA_Breach`
Isolates SLA-breached claims with full dimensional context for root-cause analysis — including region, product, claim type, and settlement duration.

```sql
CREATE VIEW vw_Claims_SLA_Breach AS
SELECT
    f.claim_id,
    d.date                                     AS claim_date,
    r.region_name,
    p.product_name,
    ct.claim_type,
    ct.severity_band,
    f.claim_amount,
    f.settlement_days,
    f.handler_id
FROM fact_Claims f
JOIN dim_Date      d  ON f.date_key       = d.date_key
JOIN dim_Region    r  ON f.region_key     = r.region_key
JOIN dim_Product   p  ON f.product_key    = p.product_key
JOIN dim_ClaimType ct ON f.claim_type_key = ct.claim_type_key
WHERE f.sla_breached = 1;
```

---

## Power BI Dashboard

A two-page interactive Power BI dashboard was built on top of the SQL MI views, using DAX measures and Power Query (M) for data transformation.

### Page 1 — Claims KPI Overview
- **KPI Cards:** Total Claims, Total Cost, Avg Settlement Days, SLA Breach Rate
- **Monthly Claims Volume Trend** (line chart)
- **Claims Cost by Region** (bar chart)
- **MoM and YoY variance** using DAX time intelligence
- Slicers: Year, Region, Product Line

### Page 2 — SLA & Leakage Deep-Dive
- **SLA Breach Rate by Region** (clustered bar)
- **SLA Breach Rate by Product Line** (heatmap table)
- **Avg Settlement Days vs SLA Threshold** (combo chart)
- **Top 10 Highest-Cost Breached Claims** (table with conditional formatting)
- **Claims Leakage Scatter** (cost vs. settlement days coloured by breach status)

### Key DAX Measures
```dax
Total Claims = COUNTROWS(fact_Claims)

SLA Breach Rate % =
DIVIDE(
    CALCULATE(COUNTROWS(fact_Claims), fact_Claims[sla_breached] = 1),
    COUNTROWS(fact_Claims)
) * 100

Avg Settlement Days = AVERAGE(fact_Claims[settlement_days])

MoM Claims Change % =
VAR current = [Total Claims]
VAR prior   = CALCULATE([Total Claims], DATEADD(dim_Date[date], -1, MONTH))
RETURN DIVIDE(current - prior, prior) * 100
```

---

## Excel MI Report

A structured Excel MI report was built for operational leadership, featuring:

- **Summary Dashboard tab** — High-level KPIs with traffic-light RAG status
- **Monthly Trends tab** — PivotTable with MoM claims volume and cost trends
- **Regional Breakdown tab** — Sortable table of KPIs by region with conditional formatting
- **Product Performance tab** — Claims and SLA metrics by product line
- **SLA Breach Log tab** — Filtered view of breached claims with handler detail
- Named ranges, structured tables, and dynamic charts throughout

---

## Key Insights & Recommendations

### Findings
| Region / Product | Issue | Impact |
|-----------------|-------|--------|
| North West | Highest SLA breach rate (38%) | Extended settlement times, customer dissatisfaction |
| Motor — Comprehensive | Longest avg settlement (47 days vs 30-day SLA) | Significant leakage risk |
| Scotland | Highest avg claim cost (+22% above national avg) | Disproportionate cost exposure |
| Home — Buildings | Rising MoM breach rate (+6pp over 3 months) | Worsening trend requiring intervention |

### Recommendations
1. **North West region** — Deploy targeted handler capacity review; introduce weekly SLA breach escalation reporting
2. **Motor Comprehensive** — Review triage workflow; consider fast-track settlement for sub-threshold claims
3. **Scotland** — Audit high-value claims for fraud indicators; reassess reserve adequacy
4. **Home Buildings** — Investigate supplier/assessor bottlenecks causing rising breach trend; consider panel review

---

## Tools & Technologies

| Tool | Usage |
|------|-------|
| **SQL Server** | Star schema design, fact/dimension tables, MI views |
| **Power BI** | Two-page interactive dashboard, DAX measures, Power Query (M) |
| **DAX** | KPI measures, time intelligence (MoM, YoY), SLA calculations |
| **Power Query (M)** | Data transformation, type casting, column renaming |
| **Excel** | MI report, PivotTables, conditional formatting, RAG dashboards |
| **Python** | Data generation, exploratory analysis, statistical summaries |

---

## Repository Structure

```
uk-insurance-market-statistics-insights-portal/
|
|-- sql/
|   |-- schema/
|   |   |-- create_star_schema.sql        # Fact and dimension table DDL
|   |   |-- insert_sample_data.sql        # Sample data population
|   |-- views/
|       |-- vw_Claims_KPI_By_Month_Region.sql
|       |-- vw_Claims_By_Product.sql
|       |-- vw_Claims_SLA_Breach.sql
|
|-- powerbi/
|   |-- UK_Insurance_Insights_Portal.pbix # Power BI dashboard file
|   |-- dashboard_screenshots/            # PNG exports of each page
|
|-- excel/
|   |-- UK_Claims_MI_Report.xlsx          # Excel MI report
|
|-- python/
|   |-- data_generation.py               # Synthetic data generation script
|   |-- eda_claims_analysis.py           # Exploratory data analysis
|   |-- requirements.txt
|
|-- docs/
|   |-- business_questions.md            # Defined questions for Head of Claims Ops
|   |-- star_schema_diagram.png          # ERD / schema diagram
|   |-- insights_and_recommendations.md  # Full findings write-up
|
|-- README.md
|-- LICENSE
```

---

## How to Use

1. **SQL Setup**
   - Run `sql/schema/create_star_schema.sql` to create tables
   - Run `sql/schema/insert_sample_data.sql` to populate with sample data
   - Execute view scripts in `sql/views/` to create MI views

2. **Power BI**
   - Open `powerbi/UK_Insurance_Insights_Portal.pbix` in Power BI Desktop
   - Update the SQL Server connection string to point to your local instance
   - Refresh data and explore the two-page dashboard

3. **Excel**
   - Open `excel/UK_Claims_MI_Report.xlsx`
   - Refresh PivotTables if connected to a live data source

4. **Python**
   - Install dependencies: `pip install -r python/requirements.txt`
   - Run `python/data_generation.py` to regenerate synthetic claims data
   - Run `python/eda_claims_analysis.py` for exploratory analysis outputs

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

*Built as a portfolio project demonstrating end-to-end insurance analytics capability — from SQL data modelling and MI view design through to Power BI dashboarding and Excel MI reporting, aligned with UK insurance market standards.*
