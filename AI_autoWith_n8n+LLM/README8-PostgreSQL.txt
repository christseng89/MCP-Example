## SQL to create table and import CSV data

CREATE TABLE energy (
    ticker TEXT,
    currency TEXT,
    price TEXT,
    market_cap_b TEXT,
    analyst TEXT,
    rating TEXT,
    target_price TEXT,
    dividend_yield TEXT,
    implied_return TEXT,
    e2023_fcf_m TEXT,
    e2023_prod_boe_d TEXT,
    e2023_gas TEXT,
    e2023_oil TEXT,
    e2023_cf_netbacks TEXT,
    e2023_cash_costs TEXT,
    e2023_eps TEXT,
    e2023_dps TEXT,
    e2023_payout TEXT,
    e2023_ndebt_ebitda TEXT,
    e2023_fcf_yield TEXT,
    e2023_evs_ebitda TEXT,
    e2023_p_e TEXT,
    e2023_div_yield TEXT,
    e2024_fcf_m TEXT,
    e2024_prod_boe_d TEXT,
    e2024_gas TEXT,
    e2024_oil TEXT,
    e2024_cf_netbacks TEXT,
    e2024_cash_costs TEXT,
    e2024_eps TEXT,
    e2024_dps TEXT
);


copy energy FROM 'C:/NorthAmericaEnergyFuturePricing.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', QUOTE '"', ENCODING 'UTF8');

//ALTER TABLE energy ALTER COLUMN Price TYPE NUMERIC USING REGEXP_REPLACE(Price, '[$,]', '', 'g')::NUMERIC;
//ALTER TABLE energy ALTER COLUMN Dividend_Yield TYPE NUMERIC USING REGEXP_REPLACE(Dividend_Yield, '[%]', '', 'g')::NUMERIC;

## CONFIG

SHOW config_file;
