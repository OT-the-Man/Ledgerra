import json
import glob
import sqlite3
import pandas as pd

conn = sqlite3.connect("ledgerra.db")

# Countries table
with open("data/raw/countries.json") as f:
    countries = json.load(f)
countries_df = pd.DataFrame(countries)
countries_df.to_sql("countries", conn, if_exists="replace", index=False)
print(f"countries: {len(countries_df)} rows")

# Observations table — every pulled indicator/country file combined
all_rows = []
for filepath in glob.glob("data/raw/*.json"):
    if filepath.endswith("countries.json"):
        continue
    with open(filepath) as f:
        raw = json.load(f)
    rows = raw.get("data", [])
    for row in rows:
        row["indicator_id"] = raw["indicator_id"]
        row["country_code"] = raw["country_code"]
    all_rows.extend(rows)

obs_df = pd.DataFrame(all_rows)
obs_df.to_sql("observations", conn, if_exists="replace", index=False)
print(f"observations: {len(obs_df)} rows")

conn.close()