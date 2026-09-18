import sqlite3
import pandas as pd

conn = sqlite3.connect("ledgerra.db")

print("=== GDP growth via SQL window function (LAG) ===")
sql = """
SELECT country_code, year, value AS gdp_usd,
       LAG(value) OVER (PARTITION BY country_code ORDER BY year) AS prev_year_gdp,
       ROUND(
         (value - LAG(value) OVER (PARTITION BY country_code ORDER BY year))
         / LAG(value) OVER (PARTITION BY country_code ORDER BY year) * 100, 2
       ) AS gdp_growth_pct
FROM observations
WHERE indicator_id = 'NY.GDP.MKTP.CD'
ORDER BY country_code, year
"""
print(pd.read_sql(sql, conn).to_string())

print("\n=== Best GDP growth year, per country (CTE) ===")
sql2 = """
WITH growth AS (
    SELECT country_code, year, value AS gdp_usd,
           LAG(value) OVER (PARTITION BY country_code ORDER BY year) AS prev_year_gdp,
           ROUND(
             (value - LAG(value) OVER (PARTITION BY country_code ORDER BY year))
             / LAG(value) OVER (PARTITION BY country_code ORDER BY year) * 100, 2
           ) AS gdp_growth_pct
    FROM observations
    WHERE indicator_id = 'NY.GDP.MKTP.CD'
)
SELECT country_code, year, gdp_growth_pct
FROM growth
WHERE gdp_growth_pct = (
    SELECT MAX(gdp_growth_pct) FROM growth AS g2 WHERE g2.country_code = growth.country_code
)
ORDER BY gdp_growth_pct DESC
"""
print(pd.read_sql(sql2, conn).to_string())

conn.close()