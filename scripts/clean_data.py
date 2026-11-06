
from pathlib import Path
import pandas as pd

# 1. Load raw dataset
df = pd.read_csv(
    "data/college_earnings_raw.csv",
    dtype={"cip_code": "string"}
)

print("Original observations:", len(df))

# 2. Keep public and private nonprofit universities
df = df[
    df["institution_type"].isin([
        "Public",
        "Private, nonprofit"
    ])
].copy()

# 3. Convert earnings to numeric
earnings_cols = [
    "median_earnings_4yr",
    "national_median_earnings_4yr"
]

for col in earnings_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 4. Keep programs with observed institutional earnings
df = df.dropna(subset=["median_earnings_4yr"]).copy()

# 5. Create broad major categories using CIP codes
df["cip_code"] = df["cip_code"].str.zfill(4)
df["cip2"] = df["cip_code"].str[:2]

major_categories = {
    "11": "Computer Science",
    "14": "Engineering",
    "45": "Social Sciences",
    "42": "Psychology",
    "23": "English",
    "52": "Business",
    "26": "Biological Sciences",
    "27": "Mathematics",
    "40": "Physical Sciences",
    "13": "Education",
    "50": "Visual and Performing Arts",
    "09": "Communication",
    "51": "Health Professions"
}

df["major_category"] = (
    df["cip2"]
    .map(major_categories)
    .fillna("Other")
)

# 6. Calculate difference from national earnings
df["earnings_difference"] = (
    df["median_earnings_4yr"]
    - df["national_median_earnings_4yr"]
)

# 7. Create an earnings-to-national ratio
df["earnings_ratio"] = (
    df["median_earnings_4yr"]
    / df["national_median_earnings_4yr"]
)

# 8. Save processed dataset
output = Path("data/college_earnings_clean.csv")
df.to_csv(output, index=False)

# 9. Print summaries
print("\nCLEANED DATASET")
print("-------------------------")
print("Observations:", len(df))
print("Universities:", df["unitid"].nunique())
print("Features:", len(df.columns))

print("\nInstitution types:")
print(df["institution_type"].value_counts())

print("\nMajor categories:")
print(df["major_category"].value_counts())

print("\nMissing values:")
print(df.isna().sum())

print("\nEarnings summary:")
print(df["median_earnings_4yr"].describe())

print("\nSaved to:", output)
