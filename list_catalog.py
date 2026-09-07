import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("AFRICA_DB_API_KEY")
BASE_URL = "https://api.africadb.com/api/v1"
headers = {"Authorization": f"Bearer {API_KEY}"}

indicators = requests.get(f"{BASE_URL}/indicators", headers=headers)
print("Indicators status:", indicators.status_code)
print(indicators.json())

countries = requests.get(f"{BASE_URL}/countries", headers=headers)
print("\nCountries status:", countries.status_code)
print(countries.json())