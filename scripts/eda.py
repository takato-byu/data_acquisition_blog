
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned dataset
df = pd.read_csv("data/college_earnings_clean.csv")

Path("figures").mkdir(exist_ok=True)

sns.set_theme(style="whitegrid")

# ------------------------------------
# 1. Earnings by major category
# ------------------------------------

major_summary = (
    df.groupby("major_category")["median_earnings_4yr"]
    .agg(["count", "median", "mean"])
    .sort_values("median", ascending=False)
)

print("\nEARNINGS BY MAJOR")
print(major_summary.round(2).to_string())

plt.figure(figsize=(11, 7))

sns.barplot(
    data=df,
    x="median_earnings_4yr",
    y="major_category",
    estimator="median",
    errorbar=None,
    order=major_summary.index
)

plt.title("Median Program Earnings by Major Category")
plt.xlabel("Median Earnings 4 Years After Completion (USD)")
plt.ylabel("Major Category")
plt.tight_layout()

plt.savefig(
    "figures/earnings_by_major.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

# ------------------------------------
# 2. Public vs. Private Universities
# ------------------------------------

institution_summary = (
    df.groupby("institution_type")["median_earnings_4yr"]
    .agg(["count", "median", "mean"])
)

print("\nEARNINGS BY INSTITUTION TYPE")
print(institution_summary.round(2).to_string())

plt.figure(figsize=(9, 6))

sns.boxplot(
    data=df,
    x="institution_type",
    y="median_earnings_4yr",
    showfliers=False
)

plt.title("Program Earnings: Public vs. Private Universities")
plt.xlabel("Institution Type")
plt.ylabel("Median Earnings (USD)")
plt.tight_layout()

plt.savefig(
    "figures/public_vs_private.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

# ------------------------------------
# 3. Earnings variation across majors
# ------------------------------------

plt.figure(figsize=(12, 8))

sns.boxplot(
    data=df,
    x="median_earnings_4yr",
    y="major_category",
    order=major_summary.index,
    showfliers=False
)

plt.title("Distribution of Program Earnings Across Majors")
plt.xlabel("Median Earnings (USD)")
plt.ylabel("Major Category")
plt.tight_layout()

plt.savefig(
    "figures/earnings_distribution.png",
    dpi=300,
    bbox_inches="tight"
)
plt.close()

print("\nEDA complete!")
print("Three figures saved to figures/")



# ------------------------------------
# 4. Earnings by major and institution type
# ------------------------------------

comparison = (
    df.groupby(["major_category", "institution_type"])
    ["median_earnings_4yr"]
    .agg(["count", "median"])
    .reset_index()
)

print("\nEARNINGS BY MAJOR AND INSTITUTION TYPE")
print(comparison.to_string(index=False))

# Use consistent category and institution ordering
major_order = major_summary.index.tolist()
type_order = sorted(df["institution_type"].dropna().unique())

# Create grouped horizontal bar chart
fig, ax = plt.subplots(figsize=(14, 9))

sns.barplot(
    data=df,
    x="median_earnings_4yr",
    y="major_category",
    hue="institution_type",
    estimator="median",
    errorbar=None,
    order=major_order,
    hue_order=type_order,
    ax=ax
)

# Add sample size labels (n) to each bar
for container, institution_type in zip(ax.containers, type_order):

    counts = (
        comparison[comparison["institution_type"] == institution_type]
        .set_index("major_category")["count"]
        .reindex(major_order)
    )

    labels = [
        f"n={int(n)}" if pd.notna(n) and n > 0 else ""
        for n in counts
    ]

    ax.bar_label(
        container,
        labels=labels,
        label_type="edge",
        padding=3,
        fontsize=8
    )

# Add extra space for labels
ax.set_xlim(0, df["median_earnings_4yr"].max() * 1.15)

ax.set_title(
    "Median Program Earnings by Major and Institution Type"
)
ax.set_xlabel("Median Earnings 4 Years After Completion (USD)")
ax.set_ylabel("Major Category")
ax.legend(title="Institution Type")

plt.tight_layout()

plt.savefig(
    "figures/earnings_by_major_and_type.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nFourth figure saved with sample sizes!")
