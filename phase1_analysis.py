import sqlite3
import pandas as pd

conn = sqlite3.connect("ledgerra.db")

print("=== Q1: Highest GDP, most recent year ===")
sql1 = """
SELECT country_code, year, value AS gdp_usd
FROM observations
WHERE indicator_id = 'NY.GDP.MKTP.CD'
  AND year = (SELECT MAX(year) FROM observations WHERE indicator_id = 'NY.GDP.MKTP.CD')
ORDER BY value DESC
"""
print(pd.read_sql(sql1, conn).to_string())

print("\n=== Q2: Average tax revenue (% of GDP) per country ===")
sql2 = """
SELECT country_code, AVG(value) AS avg_tax_pct_gdp, COUNT(*) AS num_years
FROM observations
WHERE indicator_id = 'GC.TAX.TOTL.GD.ZS'
GROUP BY country_code
ORDER BY avg_tax_pct_gdp DESC
"""
print(pd.read_sql(sql2, conn).to_string())


print("\n=== Q3: Population growth, first to last year ===")
sql3 = """
SELECT a.country_code,
       a.year AS start_year, a.value AS start_pop,
       b.year AS end_year, b.value AS end_pop,
       ROUND((b.value - a.value) / a.value * 100, 2) AS pct_growth
FROM observations a
JOIN observations b ON a.country_code = b.country_code
WHERE a.indicator_id = 'SP.POP.TOTL' AND b.indicator_id = 'SP.POP.TOTL'
  AND a.year = (SELECT MIN(year) FROM observations WHERE indicator_id = 'SP.POP.TOTL')
  AND b.year = (SELECT MAX(year) FROM observations WHERE indicator_id = 'SP.POP.TOTL')
ORDER BY pct_growth DESC
"""
print(pd.read_sql(sql3, conn).to_string())

print("\n=== Q4: GDP by country, with income group ===")
sql4 = """
SELECT o.country_code, c.name, c.income_group, o.year, o.value AS gdp_usd
FROM observations o
JOIN countries c ON o.country_code = c.code
WHERE o.indicator_id = 'NY.GDP.MKTP.CD'
  AND o.year = (SELECT MAX(year) FROM observations WHERE indicator_id = 'NY.GDP.MKTP.CD')
ORDER BY o.value DESC
"""
print(pd.read_sql(sql4, conn).to_string())

print("\n=== Q5: Combined West Africa GDP by year ===")
sql5 = """
SELECT c.region, o.year, SUM(o.value) AS total_gdp
FROM observations o
JOIN countries c ON o.country_code = c.code
WHERE o.indicator_id = 'NY.GDP.MKTP.CD'
GROUP BY c.region, o.year
ORDER BY o.year
"""
print(pd.read_sql(sql5, conn).to_string())


print("\n=== Q6: Data completeness per country ===")
sql6 = """
SELECT country_code,
       COUNT(*) AS total_rows,
       COUNT(DISTINCT indicator_id) AS indicators_present
FROM observations
GROUP BY country_code
ORDER BY total_rows DESC
"""
print(pd.read_sql(sql6, conn).to_string())

print("\n=== Q7: GDP per capita ===")
sql7 = """
SELECT g.country_code, g.year, g.value AS gdp_usd, p.value AS population,
       ROUND(g.value / p.value, 2) AS gdp_per_capita
FROM observations g
JOIN observations p ON g.country_code = p.country_code AND g.year = p.year
WHERE g.indicator_id = 'NY.GDP.MKTP.CD' AND p.indicator_id = 'SP.POP.TOTL'
ORDER BY g.year DESC, gdp_per_capita DESC
"""
print(pd.read_sql(sql7, conn).to_string())

print("\n=== Q8: Tax revenue vs GDP growth pattern ===")
sql8 = """
SELECT t.country_code, t.year, t.value AS tax_pct_gdp, g.value AS gdp_usd
FROM observations t
JOIN observations g ON t.country_code = g.country_code AND t.year = g.year
WHERE t.indicator_id = 'GC.TAX.TOTL.GD.ZS' AND g.indicator_id = 'NY.GDP.MKTP.CD'
ORDER BY t.country_code, t.year
"""
df8 = pd.read_sql(sql8, conn)
df8["gdp_growth_pct"] = df8.groupby("country_code")["gdp_usd"].pct_change() * 100
print(df8.to_string())

conn.close()