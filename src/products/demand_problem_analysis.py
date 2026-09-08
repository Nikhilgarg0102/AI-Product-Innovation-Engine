import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# PROJECT PATH
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

FEATURES_DIR = PROJECT_ROOT / "data" / "features"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

performance_file = FEATURES_DIR / "product_performance.csv"
complaints_file = FEATURES_DIR / "product_complaint_counts.csv"
reviews_file = FEATURES_DIR / "product_review_analysis.csv"
products_file = PROCESSED_DIR / "products_clean.csv"


performance = pd.read_csv(performance_file)
complaints = pd.read_csv(complaints_file)
reviews = pd.read_csv(reviews_file)
products = pd.read_csv(products_file)


print("Data loaded successfully.")
print(f"Products: {len(products)}")
print(f"Performance records: {len(performance)}")
print(f"Complaint records: {len(complaints)}")
print(f"Review records: {len(reviews)}")


# ---------------------------------------------------------
# SELECT REQUIRED COLUMNS
# ---------------------------------------------------------

performance = performance[
    ["product_id", "total_sales"]
]

complaints = complaints[
    ["product_id", "complaint_count"]
]

reviews = reviews[
    [
        "product_id",
        "negative_percentage",
        "average_rating"
    ]
]


# ---------------------------------------------------------
# MERGE PRODUCT INTELLIGENCE
# ---------------------------------------------------------

analysis = products[
    [
        "product_id",
        "product_name",
        "category",
        "subcategory",
        "price",
        "rating",
        "total_sales",
        "return_rate"
    ]
].copy()


analysis = analysis.merge(
    complaints,
    on="product_id",
    how="left"
)

analysis = analysis.merge(
    reviews,
    on="product_id",
    how="left",
    suffixes=("", "_review")
)


# ---------------------------------------------------------
# HANDLE MISSING VALUES
# ---------------------------------------------------------

analysis["complaint_count"] = (
    analysis["complaint_count"]
    .fillna(0)
)

analysis["negative_percentage"] = (
    analysis["negative_percentage"]
    .fillna(0)
)

analysis["average_rating"] = (
    analysis["average_rating"]
    .fillna(analysis["rating"])
)


# ---------------------------------------------------------
# DEMAND SCORE
# ---------------------------------------------------------

max_sales = analysis["total_sales"].max()

if max_sales > 0:
    analysis["demand_score"] = (
        analysis["total_sales"] / max_sales
    ) * 100
else:
    analysis["demand_score"] = 0


# ---------------------------------------------------------
# PROBLEM SCORE
# ---------------------------------------------------------

max_complaints = analysis["complaint_count"].max()

if max_complaints > 0:
    analysis["problem_score"] = (
        analysis["complaint_count"] / max_complaints
    ) * 100
else:
    analysis["problem_score"] = 0


# ---------------------------------------------------------
# NEGATIVE REVIEW SCORE
# ---------------------------------------------------------

analysis["negative_review_score"] = (
    analysis["negative_percentage"]
)


# ---------------------------------------------------------
# DEMAND + PROBLEM SCORE
# ---------------------------------------------------------

analysis["demand_problem_score"] = (
    0.45 * analysis["demand_score"]
    + 0.35 * analysis["problem_score"]
    + 0.20 * analysis["negative_review_score"]
)


# ---------------------------------------------------------
# PRODUCT OPPORTUNITY CATEGORY
# ---------------------------------------------------------

def classify_product(row):

    demand = row["demand_score"]
    problem = row["problem_score"]

    if demand >= 70 and problem >= 70:
        return "High Demand + High Problem"

    elif demand >= 70 and problem < 40:
        return "High Demand + Low Problem"

    elif demand < 40 and problem >= 70:
        return "Low Demand + High Problem"

    elif demand < 40 and problem < 40:
        return "Low Demand + Low Problem"

    else:
        return "Moderate"


analysis["demand_problem_category"] = (
    analysis.apply(
        classify_product,
        axis=1
    )
)


# ---------------------------------------------------------
# ROUND VALUES
# ---------------------------------------------------------

numeric_columns = [
    "demand_score",
    "problem_score",
    "negative_review_score",
    "demand_problem_score",
    "average_rating"
]

for column in numeric_columns:
    analysis[column] = analysis[column].round(2)


# ---------------------------------------------------------
# SORT BY OPPORTUNITY SCORE
# ---------------------------------------------------------

analysis = analysis.sort_values(
    "demand_problem_score",
    ascending=False
)


# ---------------------------------------------------------
# SAVE RESULT
# ---------------------------------------------------------

output_file = (
    FEATURES_DIR /
    "product_demand_problem.csv"
)

analysis.to_csv(
    output_file,
    index=False
)


# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------

print("\n" + "=" * 70)
print("TOP PRODUCT OPPORTUNITIES")
print("=" * 70)

print(
    analysis[
        [
            "product_name",
            "category",
            "total_sales",
            "complaint_count",
            "negative_percentage",
            "demand_problem_score",
            "demand_problem_category"
        ]
    ].head(10).to_string(index=False)
)


print("\n" + "=" * 70)
print("CATEGORY DISTRIBUTION")
print("=" * 70)

print(
    analysis["demand_problem_category"]
    .value_counts()
)


print("\n" + "=" * 70)
print("OUTPUT")
print("=" * 70)

print(f"Saved to: {output_file}")