import json
import pandas as pd

with open("data/raw/gdp_ghana.json") as f:
    raw = json.load(f)

print("Top-level keys:", raw.keys())
print("Indicator:", raw["indicator_id"])
print("Country:", raw["country_code"])

df = pd.DataFrame(raw["data"])
print(df.head())
print(df.dtypes)
print(df.shape)
print("Missing values per column:\n", df.isna().sum())