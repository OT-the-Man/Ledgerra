import sqlite3
import pandas as pd

conn = sqlite3.connect("ledgerra.db")
obs_df = pd.read_sql("SELECT * FROM observations", conn)
obs_df.to_csv("data/observations_export.csv", index=False)
print(f"Exported {len(obs_df)} rows to data/observations_export.csv")
conn.close()