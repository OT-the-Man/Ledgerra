import json
import sqlite3
import pandas as pd

with open("data/raw/gdp_ghana.json") as f:
    raw = json.load(f)

df = pd.DataFrame(raw["data"])
df["indicator_id"] = raw["indicator_id"]
df["country_code"] = raw["country_code"]

conn = sqlite3.connect("ledgerra.db")
df.to_sql("observations", conn, if_exists="replace", index=False)

result = pd.read_sql("SELECT * FROM observations LIMIT 5", conn)
print(result)

conn.close()