
import os
import requests
import json

api_key = os.getenv("COLLEGE_SCORECARD_API_KEY")

if not api_key:
    raise ValueError("API key is missing.")

url = "https://api.data.gov/ed/collegescorecard/v1/schools"

params = {
    "api_key": api_key,
    "id": 100654,
    "fields": "id,latest.school.name,latest.programs.cip_4_digit",
    "per_page": 1,
}

response = requests.get(url, params=params, timeout=60)

print("Status code:", response.status_code)
response.raise_for_status()

data = response.json()

if not data.get("results"):
    raise ValueError("No records returned.")

record = data["results"][0]

print("Available keys:", list(record.keys()))

print(json.dumps(
    record,
    indent=2,
    ensure_ascii=False
)[:5000])


import pandas as pd

records = []

for school in data["results"]:
    programs = school.get("latest.programs.cip_4_digit") or []

    for program in programs:
        credential = program.get("credential") or {}

        # Keep only bachelor's degree programs.
        if credential.get("level") != 3:
            continue

        earnings = program.get("earnings") or {}
        earnings_4yr = earnings.get("4_yr") or {}
        school_info = program.get("school") or {}

        records.append({
            "unitid": school["id"],
            "university": school.get("latest.school.name"),
            "cip_code": program.get("code"),
            "major": program.get("title"),
            "degree": credential.get("title"),
            "institution_type": school_info.get("type"),
            "median_earnings_4yr": earnings_4yr.get(
                "overall_median_earnings"
            ),
            "national_median_earnings_4yr": earnings_4yr.get(
                "overall_median_earnings_national"
            ),
        })

df = pd.DataFrame(records)

print("\nBachelor's degree programs:")
print(df.head(10).to_string(index=False))

print("\nNumber of programs:", len(df))
print("\nMissing values:")
print(df.isna().sum())

