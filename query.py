import sqlite3
import pandas as pd

conn = sqlite3.connect("ledgerra.db")

sql = """
SELECT indicator_id, country_code, COUNT(*) AS num_years
FROM observations
GROUP BY indicator_id, country_code
ORDER BY indicator_id, country_code
"""

result = pd.read_sql(sql, conn)
print(result.to_string())

conn.close()