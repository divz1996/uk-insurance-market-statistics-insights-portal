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

