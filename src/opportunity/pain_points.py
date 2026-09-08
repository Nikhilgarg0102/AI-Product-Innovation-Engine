import pandas as pd
from pathlib import Path


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
FEATURES_DIR = PROJECT_ROOT / "data" / "features"


# =========================================================
# LOAD DATA
# =========================================================

complaints = pd.read_csv(
    PROCESSED_DIR / "complaints_clean.csv"
)

products = pd.read_csv(
    PROCESSED_DIR / "products_clean.csv"
)

demand_problem = pd.read_csv(
    FEATURES_DIR / "product_demand_problem.csv"
)


print("=" * 70)
print("OPPORTUNITY DISCOVERY ENGINE")
print("CUSTOMER PAIN POINT ANALYSIS")
print("=" * 70)

print(f"Complaints loaded: {len(complaints)}")
print(f"Products loaded: {len(products)}")
print(f"Demand/problem records: {len(demand_problem)}")


# =========================================================
# COMPLAINT CATEGORY ANALYSIS
# =========================================================

category_analysis = (
    complaints
    .groupby("complaint_category")
    .agg(
        complaint_count=("complaint_id", "count")
    )
    .reset_index()
)


total_complaints = category_analysis["complaint_count"].sum()


category_analysis["complaint_percentage"] = (
    category_analysis["complaint_count"]
    / total_complaints
) * 100


# =========================================================
# PRIORITY ANALYSIS
# =========================================================

priority_analysis = (
    complaints
    .groupby(
        ["complaint_category", "priority"]
    )
    .size()
    .reset_index(
        name="priority_count"
    )
)


# =========================================================
# HIGH PRIORITY COMPLAINTS
# =========================================================

high_priority = complaints[
    complaints["priority"].isin(
        ["High", "Critical"]
    )
]


high_priority_analysis = (
    high_priority
    .groupby("complaint_category")
    .size()
    .reset_index(
        name="high_priority_count"
    )
)


# =========================================================
# MERGE PRIORITY INFORMATION
# =========================================================

category_analysis = category_analysis.merge(
    high_priority_analysis,
    on="complaint_category",
    how="left"
)


category_analysis["high_priority_count"] = (
    category_analysis["high_priority_count"]
    .fillna(0)
)


# =========================================================
# PAIN POINT SCORE
# =========================================================

max_complaints = (
    category_analysis["complaint_count"].max()
)

max_high_priority = (
    category_analysis["high_priority_count"].max()
)


if max_complaints > 0:

    category_analysis["volume_score"] = (
        category_analysis["complaint_count"]
        / max_complaints
    ) * 100

else:

    category_analysis["volume_score"] = 0


if max_high_priority > 0:

    category_analysis["severity_score"] = (
        category_analysis["high_priority_count"]
        / max_high_priority
    ) * 100

else:

    category_analysis["severity_score"] = 0


category_analysis["pain_point_score"] = (
    0.60 * category_analysis["volume_score"]
    + 0.40 * category_analysis["severity_score"]
)


# =========================================================
# PAIN POINT CLASSIFICATION
# =========================================================

def classify_pain_point(score):

    if score >= 75:
        return "Critical Pain Point"

    elif score >= 50:
        return "High Pain Point"

    elif score >= 25:
        return "Moderate Pain Point"

    else:
        return "Low Pain Point"


category_analysis["pain_point_level"] = (
    category_analysis["pain_point_score"]
    .apply(classify_pain_point)
)


# =========================================================
# ROUND VALUES
# =========================================================

numeric_columns = [
    "complaint_percentage",
    "volume_score",
    "severity_score",
    "pain_point_score"
]

for column in numeric_columns:

    category_analysis[column] = (
        category_analysis[column]
        .round(2)
    )


# =========================================================
# SORT PAIN POINTS
# =========================================================

category_analysis = category_analysis.sort_values(
    "pain_point_score",
    ascending=False
)


# =========================================================
# PRODUCT-LEVEL PAIN POINTS
# =========================================================

product_pain_points = (
    complaints
    .groupby(
        [
            "product_id",
            "complaint_category"
        ]
    )
    .size()
    .reset_index(
        name="complaint_count"
    )
)


product_pain_points = product_pain_points.merge(
    products[
        [
            "product_id",
            "product_name",
            "category",
            "subcategory"
        ]
    ],
    on="product_id",
    how="left"
)


# =========================================================
# ADD PRODUCT OPPORTUNITY SCORE
# =========================================================

product_pain_points = product_pain_points.merge(
    demand_problem[
        [
            "product_id",
            "demand_problem_score",
            "demand_problem_category"
        ]
    ],
    on="product_id",
    how="left"
)


# =========================================================
# PRODUCT PAIN SCORE
# =========================================================

max_product_complaints = (
    product_pain_points["complaint_count"].max()
)


if max_product_complaints > 0:

    product_pain_points["product_pain_score"] = (
        product_pain_points["complaint_count"]
        / max_product_complaints
    ) * 100

else:

    product_pain_points["product_pain_score"] = 0


product_pain_points["product_pain_score"] = (
    product_pain_points["product_pain_score"]
    .round(2)
)


# =========================================================
# SORT PRODUCT PAIN POINTS
# =========================================================

product_pain_points = (
    product_pain_points
    .sort_values(
        [
            "product_pain_score",
            "demand_problem_score"
        ],
        ascending=False
    )
)


# =========================================================
# SAVE CATEGORY ANALYSIS
# =========================================================

category_output = (
    FEATURES_DIR /
    "pain_point_analysis.csv"
)


category_analysis.to_csv(
    category_output,
    index=False
)


# =========================================================
# SAVE PRODUCT PAIN POINTS
# =========================================================

product_output = (
    FEATURES_DIR /
    "product_pain_points.csv"
)


product_pain_points.to_csv(
    product_output,
    index=False
)


# =========================================================
# DISPLAY TOP PAIN POINTS
# =========================================================

print("\n")
print("=" * 70)
print("TOP CUSTOMER PAIN POINTS")
print("=" * 70)

print(
    category_analysis[
        [
            "complaint_category",
            "complaint_count",
            "complaint_percentage",
            "high_priority_count",
            "pain_point_score",
            "pain_point_level"
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# =========================================================
# DISPLAY PRODUCT PAIN POINTS
# =========================================================

print("\n")
print("=" * 70)
print("TOP PRODUCT-LEVEL PAIN POINTS")
print("=" * 70)

print(
    product_pain_points[
        [
            "product_name",
            "category",
            "complaint_category",
            "complaint_count",
            "product_pain_score",
            "demand_problem_score",
            "demand_problem_category"
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# =========================================================
# FINAL OUTPUT
# =========================================================

print("\n")
print("=" * 70)
print("PAIN POINT ANALYSIS COMPLETE")
print("=" * 70)

print(
    f"Category analysis saved to: {category_output}"
)

print(
    f"Product pain points saved to: {product_output}"
)