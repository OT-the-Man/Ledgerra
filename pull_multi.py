import os
import json
import sys
import requests
import boto3
from datetime import date
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AFRICA_DB_API_KEY")
BASE_URL = "https://api.africadb.com/api/v1"
headers = {"Authorization": f"Bearer {API_KEY}"}
s3 = boto3.client("s3")
BUCKET = os.environ["LEDGERRA_BUCKET"]
today = date.today().isoformat()

countries = ["GH", "NG", "CI", "SN", "ML"]
indicators = ["NY.GDP.MKTP.CD", "SP.POP.TOTL", "GC.TAX.TOTL.GD.ZS"]

os.makedirs("data/raw", exist_ok=True)

resp = requests.get(f"{BASE_URL}/countries", headers=headers)
if resp.status_code == 200:
    with open("data/raw/countries.json", "w") as f:
        json.dump(resp.json(), f, indent=2)
print(f"Countries: {resp.status_code}")

landed = set()
for page in s3.get_paginator("list_objects_v2").paginate(Bucket=BUCKET, Prefix="raw/"):
    for obj in page.get("Contents", []):
        landed.add(obj["Key"].split("/")[-1])

pairs = [(i, c) for i in indicators for c in countries]
pairs.sort(key=lambda p: f"{p[0]}_{p[1]}.json" in landed)

fetched = 0
statuses = set()

for indicator, country in pairs:
    url = f"{BASE_URL}/observations/timeseries/{indicator}/{country}"
    resp = requests.get(url, headers=headers)
    statuses.add(resp.status_code)
    filename = f"data/raw/{indicator}_{country}.json"
    if resp.status_code == 200:
        with open(filename, "w") as f:
            json.dump(resp.json(), f, indent=2)
        s3.upload_file(filename, BUCKET, f"raw/{today}/{indicator}_{country}.json")
        print(f"  Uploaded to S3: raw/{today}/{indicator}_{country}.json")
        fetched += 1
    else:
        print(f"  SKIPPED write, kept existing file")
    print(f"{indicator} / {country}: {resp.status_code}")

# Exit 99 = nothing fetched only because of the daily quota (the Airflow DAG treats it as 'skipped').
# Exit 1 = nothing fetched for any other reason (bad key, server error) = a real failure.
if fetched == 0:
    if statuses == {429}:
        print("Nothing fetched: every call was rate-limited (daily quota used up).")
        sys.exit(99)
    print(f"Nothing fetched and not only rate limits (statuses seen: {sorted(statuses)}).")
    sys.exit(1)
