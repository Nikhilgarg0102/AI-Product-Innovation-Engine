import pandas as pd
from pathlib import Path
import sys


# --------------------------------------------------
# Project root
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(str(PROJECT_ROOT))


# --------------------------------------------------
# Load data
# --------------------------------------------------

from src.preprocessing.data_loader import load_data

data = load_data()

products = data["products"]
complaints = data["complaints"]


print("=" * 70)
print("PRODUCT INTELLIGENCE ENGINE")
print("PRODUCT COMPLAINT ANALYSIS")
print("=" * 70)


# --------------------------------------------------
# Combine product information with complaints
# --------------------------------------------------

df = complaints.merge(
    products[
        [
            "product_id",
            "product_name",
            "category"
        ]
    ],
    on="product_id",
    how="left"
)


# --------------------------------------------------
# Complaint count per product
# --------------------------------------------------

product_complaint_count = (
    df.groupby(
        [
            "product_id",
            "product_name",
            "category"
        ]
    )
    .size()
    .reset_index(
        name="complaint_count"
    )
)


# --------------------------------------------------
# Complaint count by product + category
# --------------------------------------------------

product_problem_analysis = (
    df.groupby(
        [
            "product_id",
            "product_name",
            "category",
            "complaint_category"
        ]
    )
    .size()
    .reset_index(
        name="complaint_count"
    )
)


# --------------------------------------------------
# Calculate percentage of complaints
# --------------------------------------------------

product_problem_analysis["problem_percentage"] = (
    product_problem_analysis["complaint_count"]
    /
    product_problem_analysis
    .groupby("product_id")[
        "complaint_count"
    ]
    .transform("sum")
    * 100
)


# --------------------------------------------------
# Sort
# --------------------------------------------------

product_problem_analysis = (
    product_problem_analysis
    .sort_values(
        "complaint_count",
        ascending=False
    )
)


product_complaint_count = (
    product_complaint_count
    .sort_values(
        "complaint_count",
        ascending=False
    )
)


# --------------------------------------------------
# Find the biggest problem for each product
# --------------------------------------------------

main_problem = (
    product_problem_analysis
    .sort_values(
        [
            "product_id",
            "complaint_count"
        ],
        ascending=[True, False]
    )
    .drop_duplicates(
        subset=["product_id"]
    )
)


main_problem = main_problem[
    [
        "product_id",
        "product_name",
        "category",
        "complaint_category",
        "complaint_count"
    ]
]


main_problem = main_problem.rename(
    columns={
        "complaint_category":
            "main_problem",
        "complaint_count":
            "main_problem_count"
    }
)


# --------------------------------------------------
# Save outputs
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


product_complaint_count.to_csv(
    OUTPUT_DIR
    / "product_complaint_counts.csv",
    index=False
)


product_problem_analysis.to_csv(
    OUTPUT_DIR
    / "product_problem_analysis.csv",
    index=False
)


main_problem.to_csv(
    OUTPUT_DIR
    / "product_main_problems.csv",
    index=False
)


# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\nProduct complaint analysis complete.")

print(
    f"Total complaints analysed: "
    f"{len(df):,}"
)


print(
    f"Products with complaints: "
    f"{product_complaint_count['product_id'].nunique():,}"
)


print("\nTop products by complaint count:")

print(
    product_complaint_count.head(10)
)


print("\nTop product problems:")

print(
    product_problem_analysis.head(15)
)


print("\nMain problem for products:")

print(
    main_problem.head(15)
)


print("\nOutput files created:")

print(
    "product_complaint_counts.csv"
)

print(
    "product_problem_analysis.csv"
)

print(
    "product_main_problems.csv"
)


print("\n" + "=" * 70)
print("PRODUCT COMPLAINT ANALYSIS COMPLETE")
print("=" * 70)