import pandas as pd
from pathlib import Path
import sys


# --------------------------------------------------
# Project root
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(str(PROJECT_ROOT))


# --------------------------------------------------
# Import unified data loader
# --------------------------------------------------

from src.preprocessing.data_loader import load_data


# --------------------------------------------------
# Load data
# --------------------------------------------------

data = load_data()

customers = data["customers"]
purchases = data["purchases"]


print("=" * 65)
print("CUSTOMER INTELLIGENCE ENGINE")
print("CUSTOMER SEGMENTATION")
print("=" * 65)


# --------------------------------------------------
# Aggregate purchase behaviour
# --------------------------------------------------

purchase_features = (
    purchases
    .groupby("customer_id")
    .agg(
        total_orders=("purchase_id", "count"),
        total_quantity=("quantity", "sum"),
        total_spend=("unit_price", "sum"),
        average_discount=("discount", "mean")
    )
    .reset_index()
)


# --------------------------------------------------
# Merge customer information
# --------------------------------------------------

df = customers.merge(
    purchase_features,
    on="customer_id",
    how="left"
)


# --------------------------------------------------
# Fill customers without purchases
# --------------------------------------------------

numeric_columns = [
    "total_orders",
    "total_quantity",
    "total_spend",
    "average_discount"
]

df[numeric_columns] = (
    df[numeric_columns]
    .fillna(0)
)


# --------------------------------------------------
# Calculate customer value
# --------------------------------------------------

df["customer_value"] = (
    df["total_spend"] * df["total_orders"]
)


# --------------------------------------------------
# Segment customers
# --------------------------------------------------

def assign_segment(row):

    spend = row["total_spend"]
    orders = row["total_orders"]

    if spend >= 3000 and orders >= 15:
        return "Premium Loyal"

    elif spend >= 2000 and orders >= 10:
        return "High Value"

    elif orders >= 8:
        return "Frequent Buyer"

    elif spend >= 1000:
        return "Regular Buyer"

    elif orders > 0:
        return "Occasional Buyer"

    else:
        return "Inactive"


df["customer_segment"] = df.apply(
    assign_segment,
    axis=1
)


# --------------------------------------------------
# Save results
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
    / "customer_segments.csv"
)


df.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\nCustomer segmentation complete.")

print(
    f"Customers analysed: "
    f"{len(df):,}"
)

print(
    f"Output: {OUTPUT_FILE}"
)


print("\nSegment distribution:")

print(
    df["customer_segment"]
    .value_counts()
)


print("\nAverage spend by segment:")

print(
    df.groupby("customer_segment")[
        "total_spend"
    ]
    .mean()
    .sort_values(
        ascending=False
    )
)


print("\nSample customer profiles:")

print(
    df[
        [
            "customer_id",
            "age_group",
            "income_segment",
            "loyalty_level",
            "total_orders",
            "total_spend",
            "customer_segment"
        ]
    ].head(10)
)


print("\n" + "=" * 65)
print("CUSTOMER SEGMENTATION COMPLETE")
print("=" * 65)