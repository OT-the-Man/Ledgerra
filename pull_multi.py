import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AFRICA_DB_API_KEY")
BASE_URL = "https://api.africadb.com/api/v1"
headers = {"Authorization": f"Bearer {API_KEY}"}

countries = ["GH", "NG", "CI", "SN", "ML"]
indicators = ["NY.GDP.MKTP.CD", "SP.POP.TOTL", "GC.TAX.TOTL.GD.ZS"]


os.makedirs("data/raw", exist_ok=True)

# Save countries reference table once
resp = requests.get(f"{BASE_URL}/countries", headers=headers)
with open("data/raw/countries.json", "w") as f:
    json.dump(resp.json(), f, indent=2)
print(f"Countries: {resp.status_code}")

# Loop indicators x countries
for indicator in indicators:
    for country in countries:
        url = f"{BASE_URL}/observations/timeseries/{indicator}/{country}"
        resp = requests.get(url, headers=headers)
        filename = f"data/raw/{indicator}_{country}.json"
        with open(filename, "w") as f:
            json.dump(resp.json(), f, indent=2)
        print(f"{indicator} / {country}: {resp.status_code}")