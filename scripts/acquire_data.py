
import os
import time
from pathlib import Path

import pandas as pd
import requests

# API configuration
API_KEY = os.getenv("COLLEGE_SCORECARD_API_KEY")
BASE_URL = "https://api.data.gov/ed/collegescorecard/v1/schools"

if not API_KEY:
    raise ValueError("COLLEGE_SCORECARD_API_KEY is missing.")

PER_PAGE = 20
MAX_PAGES = 20

records = []

# Retrieve multiple pages of university data
for page in range(MAX_PAGES):
    params = {
        "api_key": API_KEY,
        "fields": (
            "id,latest.school.name,"
            "latest.school.state,"
            "latest.programs.cip_4_digit"
        ),
        "per_page": PER_PAGE,
        "page": page,
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=120
    )

    print(f"Page {page + 1}: HTTP {response.status_code}")
    response.raise_for_status()

    data = response.json()
    schools = data.get("results", [])

    if not schools:
        break

    for school in schools:
        programs = school.get(
            "latest.programs.cip_4_digit"
        ) or []

        for program in programs:
            credential = program.get("credential") or {}

            if credential.get("level") != 3:
                continue

            earnings = program.get("earnings") or {}
            earnings_4yr = earnings.get("4_yr") or {}
            school_info = program.get("school") or {}

            records.append({
                "unitid": school.get("id"),
                "university": school.get(
                    "latest.school.name"
                ),
                "state": school.get(
                    "latest.school.state"
                ),
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

    # Respect API rate limits
    time.sleep(0.5)

# Convert records into a DataFrame
df = pd.DataFrame(records)

if df.empty:
    raise ValueError("No bachelor's degree programs found.")

# Convert earnings to numeric values
earnings_columns = [
    "median_earnings_4yr",
    "national_median_earnings_4yr"
]

for column in earnings_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

# Remove duplicate university-major records
df = df.drop_duplicates(
    subset=["unitid", "cip_code", "degree"]
)

# Create output directory
output_dir = Path("data")
output_dir.mkdir(parents=True, exist_ok=True)

# Save dataset
output_file = output_dir / "college_earnings_raw.csv"
df.to_csv(output_file, index=False)

# Summary
print("\nDATA ACQUISITION COMPLETE")
print("-------------------------")
print("Total programs:", len(df))
print("Unique universities:", df["unitid"].nunique())
print("Number of features:", len(df.columns))

print("\nMissing values:")
print(df.isna().sum())

print("\nInstitution types:")
print(df["institution_type"].value_counts(dropna=False))

print("\nPrograms with earnings data:")
print(df["median_earnings_4yr"].notna().sum())

print("\nSaved to:", output_file)
