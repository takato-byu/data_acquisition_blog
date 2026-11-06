
import os
import requests

API_KEY = os.getenv("COLLEGE_SCORECARD_API_KEY")

if not API_KEY:
    raise ValueError("API key is missing.")

url = "https://api.data.gov/ed/collegescorecard/v1/schools"

params = {
    "api_key": API_KEY,
    "per_page": 5,
}

response = requests.get(url, params=params, timeout=30)

print("Status code:", response.status_code)
response.raise_for_status()

data = response.json()

print("Total institutions:", data.get("metadata", {}).get("total"))
print("Records returned:", len(data.get("results", [])))

for school in data.get("results", []):
    print(school["latest"]["school"]["name"])

import json

print(json.dumps(
    data["results"][0],
    indent=2,
    ensure_ascii=False
)[:3000])

import pandas as pd

schools = []

for record in data["results"]:
    school = record["latest"]["school"]

    schools.append({
        "unitid": record["id"],
        "university": school["name"],
        "state": school["state"],
        "ownership": school["ownership"],
        "city": school["city"]
    })

df = pd.DataFrame(schools)

print(df)