import pandas as pd
from pathlib import Path
import sys


# --------------------------------------------------
# Project root
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(str(PROJECT_ROOT))


# --------------------------------------------------
# Load unified data
# --------------------------------------------------

from src.preprocessing.data_loader import load_data

data = load_data()

products = data["products"]


print("=" * 70)
print("PRODUCT INTELLIGENCE ENGINE")
print("PRODUCT PERFORMANCE ANALYSIS")
print("=" * 70)


# --------------------------------------------------
# Create analysis dataset
# --------------------------------------------------

df = products.copy()


# --------------------------------------------------
# Normalize sales
# --------------------------------------------------

sales_min = df["total_sales"].min()
sales_max = df["total_sales"].max()

if sales_max > sales_min:

    df["sales_score"] = (
        (df["total_sales"] - sales_min)
        /
        (sales_max - sales_min)
        * 100
    )

else:

    df["sales_score"] = 50


# --------------------------------------------------
# Rating score
# --------------------------------------------------

df["rating_score"] = (
    df["rating"] / 5
) * 100


# --------------------------------------------------
# Return score
# Lower return rate = better
# --------------------------------------------------

return_min = df["return_rate"].min()
return_max = df["return_rate"].max()

if return_max > return_min:

    df["return_score"] = (
        1
        -
        (
            (df["return_rate"] - return_min)
            /
            (return_max - return_min)
        )
    ) * 100

else:

    df["return_score"] = 50


# --------------------------------------------------
# Profit margin
# --------------------------------------------------

df["profit_margin"] = (
    (df["price"] - df["cost"])
    /
    df["price"]
) * 100


df["profit_margin"] = (
    df["profit_margin"]
    .clip(lower=0, upper=100)
)


# --------------------------------------------------
# Profitability score
# --------------------------------------------------

margin_min = df["profit_margin"].min()
margin_max = df["profit_margin"].max()

if margin_max > margin_min:

    df["profitability_score"] = (
        (df["profit_margin"] - margin_min)
        /
        (margin_max - margin_min)
        * 100
    )

else:

    df["profitability_score"] = 50


# --------------------------------------------------
# Product performance score
# --------------------------------------------------

df["performance_score"] = (
    0.35 * df["sales_score"]
    +
    0.30 * df["rating_score"]
    +
    0.20 * df["return_score"]
    +
    0.15 * df["profitability_score"]
)


# --------------------------------------------------
# Assign performance category
# --------------------------------------------------

def performance_category(score):

    if score >= 80:
        return "Excellent"

    elif score >= 65:
        return "Strong"

    elif score >= 50:
        return "Average"

    elif score >= 35:
        return "Weak"

    else:
        return "Poor"


df["performance_category"] = (
    df["performance_score"]
    .apply(performance_category)
)


# --------------------------------------------------
# Sort products
# --------------------------------------------------

df = df.sort_values(
    "performance_score",
    ascending=False
)


# --------------------------------------------------
# Save output
# --------------------------------------------------

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "features"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


OUTPUT_FILE = (
    OUTPUT_DIR
    / "product_performance.csv"
)


df.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\nProduct performance analysis complete.")

print(
    f"Products analysed: "
    f"{len(df):,}"
)

print(
    f"Output: {OUTPUT_FILE}"
)


print("\nPerformance distribution:")

print(
    df["performance_category"]
    .value_counts()
)


print("\nAverage performance score:")

print(
    f"{df['performance_score'].mean():.2f}"
)


print("\nTop performing products:")

print(
    df[
        [
            "product_id",
            "product_name",
            "category",
            "rating",
            "total_sales",
            "return_rate",
            "profit_margin",
            "performance_score",
            "performance_category"
        ]
    ].head(10)
)


print("\nLowest performing products:")

print(
    df[
        [
            "product_id",
            "product_name",
            "category",
            "rating",
            "total_sales",
            "return_rate",
            "performance_score",
            "performance_category"
        ]
    ].tail(10)
)


print("\n" + "=" * 70)
print("PRODUCT PERFORMANCE ANALYSIS COMPLETE")
print("=" * 70)