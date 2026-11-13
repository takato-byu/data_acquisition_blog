
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ------------------------------------
# 0. Load cleaned dataset
# ------------------------------------

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

print("\nFirst three figures saved!")


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


# Define category and institution order
major_order = major_summary.index.tolist()

type_order = [
    "Public",
    "Private, nonprofit"
]


# Create grouped bar chart
fig, ax = plt.subplots(figsize=(14, 9))

sns.barplot(
    data=comparison,
    x="median",
    y="major_category",
    hue="institution_type",
    order=major_order,
    hue_order=type_order,
    errorbar=None,
    ax=ax
)


# ------------------------------------
# Add sample sizes to each bar
# ------------------------------------

counts = comparison.set_index(
    ["major_category", "institution_type"]
)["count"]

for container, institution_type in zip(
    ax.containers, type_order
):
    for major, bar in zip(
        major_order, container.patches
    ):

        n = counts.get(
            (major, institution_type), 0
        )

        if n == 0:
            continue

        width = bar.get_width()

        y = (
            bar.get_y()
            + bar.get_height() / 2
        )

        ax.text(
            width + 1500,
            y,
            f"n={int(n)}",
            va="center",
            ha="left",
            fontsize=8
        )


# ------------------------------------
# Customize chart
# ------------------------------------

ax.set_title(
    "Median Program Earnings by Major and Institution Type"
)

ax.set_xlabel(
    "Median Earnings 4 Years After Completion (USD)"
)

ax.set_ylabel("Major Category")

ax.legend(
    title="Institution Type"
)

# Add space for sample-size labels
ax.set_xlim(
    0,
    comparison["median"].max() * 1.25
)

plt.tight_layout()


# ------------------------------------
# Save chart
# ------------------------------------

plt.savefig(
    "figures/earnings_by_major_and_type.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nFourth figure saved with sample sizes!")
print("\nEDA complete! Four figures saved to figures/")
