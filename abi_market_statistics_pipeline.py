# =============================================================
# UK Insurance Market Statistics & Insights Portal (SQL + Power BI + Excel + Python)
# Author: Divyansh Dubey
# Description: I built this script to simulate ABI-style insurance market
#              statistics, subscriptions and helpdesk simulation. I clean,
#              model and push a star schema ready for SQL and Power BI reporting.
# =============================================================

import csv
import requests
import io
import pandas as pd
import numpy as np


# -------------------------------------------------------------
# STEP 1: Fetch and clean the raw insurance claims data
# I fetch the raw file directly from my GitHub repo using
# the requests library, then fix broken line breaks that
# were causing parsing issues in the original file.
# -------------------------------------------------------------

input_url = "https://raw.githubusercontent.com/divz1996/uk-insurance-market-statistics-insights-portal/main/data/insurance_claims_main.txt"
output_filename = "cleaned_insurance_claims.csv"

def clean_insurance_data(input_url, output_file):
    # I fetch the raw file content from my GitHub repo
    response = requests.get(input_url)
    response.raise_for_status()  # I raise an error here if the download fails
    raw_content = response.text

    # I remove surrounding quotes and fix broken line breaks within records
    lines = raw_content.replace('"\n"', '\n').replace('"\r\n"', '\n').strip('"').splitlines()
    cleaned_rows = []
    current_row = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue
        # I identify a new record by checking if the line starts with a digit or the header
        if line[0].isdigit() or line.startswith('months_as_customer'):
            if current_row:
                cleaned_rows.append(current_row)
            current_row = line
        else:
            # This is a continuation of a broken previous row - I rejoin it
            current_row += " " + line

    # I append the final record after the loop ends
    if current_row:
        cleaned_rows.append(current_row)

    # I write the cleaned rows to a CSV file
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in cleaned_rows:
            writer.writerow(row.split(','))

    print(f"Done! {len(cleaned_rows)} rows saved to: {output_file}")

clean_insurance_data(input_url, output_filename)


# -------------------------------------------------------------
# STEP 2: Load the cleaned CSV and parse dates
# I read the cleaned CSV back into a pandas DataFrame
# and convert the incident_date column to datetime format
# so I can use it to build the date dimension table.
# -------------------------------------------------------------

url = "https://raw.githubusercontent.com/divz1996/uk-insurance-market-statistics-insights-portal/main/data/cleaned_insurance_claims.csv"
df = pd.read_csv(url)
df['incident_date'] = pd.to_datetime(df['incident_date'])  # I convert the date column to datetime
print(f"Loaded {len(df)} rows, {len(df.columns)} columns")


# -------------------------------------------------------------
# STEP 3: Build dim_date
# I create a calendar dimension table that covers the full
# incident date range (January to March 2015).
# I include a date_key in YYYYMMDD integer format which I
# use to join this table to the fact table.
# -------------------------------------------------------------

dates = pd.DataFrame({'date': pd.date_range('2015-01-01', '2015-03-31')})
dates['date_key']      = dates['date'].dt.strftime('%Y%m%d').astype(int)
dates['day']           = dates['date'].dt.day
dates['month']         = dates['date'].dt.month
dates['month_name']    = dates['date'].dt.strftime('%B')
dates['quarter']       = dates['date'].dt.quarter
dates['year']          = dates['date'].dt.year
dates['financial_year'] = '2014/15'  # I add UK financial year context


# -------------------------------------------------------------
# STEP 4: Build dim_region
# I map each claim to a UK region.
# Because the source dataset is US-based, I randomly assign
# UK regions to simulate a realistic UK market distribution.
# I also group regions into broader areas and countries.
# -------------------------------------------------------------

uk_regions = [
    'North West', 'North East', 'Yorkshire and Humber', 'East Midlands',
    'West Midlands', 'East of England', 'London', 'South East',
    'South West', 'Scotland', 'Wales', 'Northern Ireland'
]
area_map = {
    'North West': 'North England', 'North East': 'North England',
    'Yorkshire and Humber': 'North England', 'East Midlands': 'Midlands',
    'West Midlands': 'Midlands', 'East of England': 'East England',
    'London': 'London', 'South East': 'South England', 'South West': 'South England',
    'Scotland': 'Scotland', 'Wales': 'Wales', 'Northern Ireland': 'Northern Ireland'
}
country_map = {
    'North West': 'England', 'North East': 'England', 'Yorkshire and Humber': 'England',
    'East Midlands': 'England', 'West Midlands': 'England', 'East of England': 'England',
    'London': 'England', 'South East': 'England', 'South West': 'England',
    'Scotland': 'Scotland', 'Wales': 'Wales', 'Northern Ireland': 'Northern Ireland'
}
dim_region = pd.DataFrame({
    'region_key':  [f'R{str(i+1).zfill(2)}' for i in range(12)],
    'region_name': uk_regions,
    'area':        [area_map[r] for r in uk_regions],
    'country':     [country_map[r] for r in uk_regions]
})


# -------------------------------------------------------------
# STEP 5: Build dim_product
# I define the insurance product lines relevant to the
# UK market, covering Motor, Home, Liability, Travel,
# Pet and Commercial insurance products.
# -------------------------------------------------------------

dim_product = pd.DataFrame([
    ('P01', 'Motor Comprehensive',              'Motor',      'Comprehensive'),
    ('P02', 'Motor Third Party Fire and Theft', 'Motor',      'TPFT'),
    ('P03', 'Motor Third Party Only',           'Motor',      'TPO'),
    ('P04', 'Home Buildings',                   'Home',       'Buildings'),
    ('P05', 'Home Contents',                    'Home',       'Contents'),
    ('P06', 'Home Combined',                    'Home',       'Combined'),
    ('P07', 'Employers Liability',              'Liability',  'Employers'),
    ('P08', 'Public Liability',                 'Liability',  'Public'),
    ('P09', 'Professional Indemnity',           'Liability',  'Professional'),
    ('P10', 'Travel Single Trip',               'Travel',     'Single Trip'),
    ('P11', 'Travel Annual Multi-Trip',         'Travel',     'Annual'),
    ('P12', 'Pet Dog',                          'Pet',        'Dog'),
    ('P13', 'Pet Cat',                          'Pet',        'Cat'),
    ('P14', 'Commercial Vehicle',               'Commercial', 'Vehicle'),
    ('P15', 'Commercial Property',              'Commercial', 'Property'),
], columns=['product_key', 'product_name', 'product_line', 'coverage_type'])


# -------------------------------------------------------------
# STEP 6: Build dim_claimtype
# I classify each claim by type and severity band.
# I use the severity band in my SLA breach analysis -
# High severity claims have a stricter SLA requirement.
# -------------------------------------------------------------

dim_claimtype = pd.DataFrame([
    ('CT01', 'Single Vehicle Collision',  'Motor',     'High'),
    ('CT02', 'Multi-vehicle Collision',   'Motor',     'High'),
    ('CT03', 'Vehicle Theft',             'Motor',     'Medium'),
    ('CT04', 'Parked Car Damage',         'Motor',     'Low'),
    ('CT05', 'Home Structural Damage',    'Home',      'High'),
    ('CT06', 'Home Contents Loss',        'Home',      'Medium'),
    ('CT07', 'Employer Liability Claim',  'Liability', 'High'),
    ('CT08', 'Public Liability Claim',    'Liability', 'Medium'),
    ('CT09', 'Travel Medical Claim',      'Travel',    'Medium'),
    ('CT10', 'Travel Cancellation',       'Travel',    'Low'),
], columns=['claim_type_key', 'claim_type', 'claim_category', 'severity_band'])


# -------------------------------------------------------------
# STEP 7: Map dimension keys onto the main DataFrame
# I randomly assign UK regions using seed=42 so my results
# are reproducible. I then map each incident type to the
# corresponding product key and claim type key.
# -------------------------------------------------------------

np.random.seed(42)
df['region_name'] = np.random.choice(uk_regions, size=len(df))
df['region_key']  = df['region_name'].map(dict(zip(dim_region['region_name'], dim_region['region_key'])))

# I map incident_type from the raw data to my product and claim type keys
incident_to_product   = {
    'Single Vehicle Collision': 'P01', 'Multi-vehicle Collision': 'P01',
    'Vehicle Theft': 'P02', 'Parked Car': 'P03'
}
incident_to_claimtype = {
    'Single Vehicle Collision': 'CT01', 'Multi-vehicle Collision': 'CT02',
    'Vehicle Theft': 'CT03', 'Parked Car': 'CT04'
}
df['product_key']    = df['incident_type'].map(incident_to_product).fillna('P01')
df['claim_type_key'] = df['incident_type'].map(incident_to_claimtype).fillna('CT01')

# I convert incident_date to an integer date_key (YYYYMMDD) for joining with dim_date
df['date_key'] = df['incident_date'].dt.strftime('%Y%m%d').astype(int)


# -------------------------------------------------------------
# STEP 8: Add SLA and settlement columns
# I simulate settlement_days between 5 and 60 days.
# My SLA threshold is 30 days, based on the standard
# UK motor claims target. I flag sla_breached = 1 if
# settlement took more than 30 days, otherwise 0.
# I also assign a handler ID to each claim (50 handlers).
# -------------------------------------------------------------

np.random.seed(99)
df['settlement_days'] = np.random.randint(5, 61, size=len(df))
df['sla_breached']    = (df['settlement_days'] > 30).astype(int)
df['handler_id']      = ['H' + str(np.random.randint(1, 51)).zfill(3) for _ in range(len(df))]


# -------------------------------------------------------------
# STEP 9: Build the fact_claims table
# I select the relevant columns from the cleaned DataFrame
# and rename them to match my star schema column names.
# claim_amount is taken from total_claim_amount in the
# raw data (injury + property + vehicle combined).
# -------------------------------------------------------------

fact_claims = df[[
    'policy_number', 'date_key', 'region_key', 'product_key', 'claim_type_key',
    'total_claim_amount', 'settlement_days', 'sla_breached', 'handler_id', 'fraud_reported'
]].copy()
fact_claims.columns = [
    'claim_id', 'date_key', 'region_key', 'product_key', 'claim_type_key',
    'claim_amount', 'settlement_days', 'sla_breached', 'handler_id', 'fraud_reported'
]


# -------------------------------------------------------------
# STEP 10: Save all five tables to CSV
# I export each dimension and the fact table as a separate
# CSV file, ready to load into SQL Server or Power BI.
# -------------------------------------------------------------

fact_claims.to_csv('fact_claims.csv',    index=False)
dim_region.to_csv('dim_region.csv',      index=False)
dim_product.to_csv('dim_product.csv',    index=False)
dim_claimtype.to_csv('dim_claimtype.csv', index=False)
dates.to_csv('dim_date.csv',             index=False)

print(f"Done! {len(fact_claims)} claims processed")
print(f"  SLA breach rate: {fact_claims['sla_breached'].mean()*100:.1f}%")
print(f"  Avg claim amount: GBP{fact_claims['claim_amount'].mean():,.0f}")
print(fact_claims.head(3))
