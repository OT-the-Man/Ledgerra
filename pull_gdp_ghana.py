import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AFRICA_DB_API_KEY")
BASE_URL = "https://api.africadb.com/api/v1"

indicator = "NY.GDP.MKTP.CD"  # GDP
country = "GH"                 # Ghana

url = f"{BASE_URL}/observations/timeseries/{indicator}/{country}"
headers = {"Authorization": f"Bearer {API_KEY}"}

response = requests.get(url, headers=headers)
response.raise_for_status()

data = response.json()

os.makedirs("data/raw", exist_ok=True)
output_path = "data/raw/gdp_ghana.json"
with open(output_path, "w") as f:
    json.dump(data, f, indent=2)

print(f"Saved to {output_path}")
print(f"Status code: {response.status_code}")