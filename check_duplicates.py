import sqlite3
import pandas as pd

conn = sqlite3.connect("ledgerra.db")

sql = """
SELECT indicator_id, country_code, year, COUNT(*) AS times_seen
FROM observations
GROUP BY indicator_id, country_code, year
HAVING COUNT(*) > 1
"""

result = pd.read_sql(sql, conn)
print(result.to_string())

conn.close()