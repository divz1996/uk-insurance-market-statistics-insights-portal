
-- ============================================================
-- UK Insurance Market Statistics - Star Schema
-- ============================================================

-- Dimension: Region
CREATE TABLE dim_region (
    region_id INT PRIMARY KEY,
    region_name VARCHAR(100)
);

-- Dimension: Product
CREATE TABLE dim_product (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100)
);

-- Dimension: Claim Type
CREATE TABLE dim_claimtype (
    claimtype_id INT PRIMARY KEY,
    claim_type VARCHAR(100)
);

-- Dimension: Date
CREATE TABLE dim_date (
    date_id INT PRIMARY KEY,
    full_date DATE,
    year INT,
    month INT,
    quarter INT,
    month_name VARCHAR(20)
);

-- Fact Table: Claims
CREATE TABLE fact_claims (
    claim_id VARCHAR(50) PRIMARY KEY,
    date_id INT REFERENCES dim_date(date_id),
    region_id INT REFERENCES dim_region(region_id),
    product_id INT REFERENCES dim_product(product_id),
    claimtype_id INT REFERENCES dim_claimtype(claimtype_id),
    claim_amount DECIMAL(12,2),
    settlement_days INT,
    sla_breach INT,  -- 1 = breached, 0 = within SLA
    leakage_amount DECIMAL(12,2)
);

-- ============================================================
-- MI Views
-- ============================================================

-- View 1: KPI by Month and Region
CREATE VIEW vw_Claims_KPI_By_Month_Region AS
SELECT
    d.year,
    d.month_name,
    r.region_name,
    COUNT(f.claim_id)          AS total_claims,
    SUM(f.claim_amount)        AS total_claim_value,
    AVG(f.settlement_days)     AS avg_settlement_days,
    SUM(f.sla_breach)          AS sla_breaches,
    ROUND(100.0 * SUM(f.sla_breach) / COUNT(f.claim_id), 2) AS sla_breach_rate_pct
FROM fact_claims f
JOIN dim_date d    ON f.date_id    = d.date_id
JOIN dim_region r  ON f.region_id  = r.region_id
GROUP BY d.year, d.month_name, r.region_name;

-- View 2: Claims by Product
CREATE VIEW vw_Claims_By_Product AS
SELECT
    p.product_name,
    COUNT(f.claim_id)          AS total_claims,
    SUM(f.claim_amount)        AS total_claim_value,
    AVG(f.settlement_days)     AS avg_settlement_days,
    SUM(f.sla_breach)          AS sla_breaches
FROM fact_claims f
JOIN dim_product p ON f.product_id = p.product_id
GROUP BY p.product_name;

-- View 3: SLA Breach Analysis
CREATE VIEW vw_Claims_SLA_Breach AS
SELECT
    r.region_name,
    p.product_name,
    ct.claim_type,
    COUNT(f.claim_id)          AS total_claims,
    SUM(f.sla_breach)          AS total_breaches,
    ROUND(100.0 * SUM(f.sla_breach) / COUNT(f.claim_id), 2) AS breach_rate_pct,
    AVG(f.settlement_days)     AS avg_settlement_days,
    SUM(f.leakage_amount)      AS total_leakage
FROM fact_claims f
JOIN dim_region r    ON f.region_id    = r.region_id
JOIN dim_product p   ON f.product_id   = p.product_id
JOIN dim_claimtype ct ON f.claimtype_id = ct.claimtype_id
WHERE f.sla_breach = 1
GROUP BY r.region_name, p.product_name, ct.claim_type;
