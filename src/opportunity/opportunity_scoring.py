import pandas as pd
from pathlib import Path


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

FEATURES_DIR = PROJECT_ROOT / "data" / "features"


# =========================================================
# LOAD DATA
# =========================================================

pain_points = pd.read_csv(
    FEATURES_DIR / "product_pain_points.csv"
)

market_gaps = pd.read_csv(
    FEATURES_DIR / "market_gap_analysis.csv"
)

demand_problem = pd.read_csv(
    FEATURES_DIR / "product_demand_problem.csv"
)


print("=" * 70)
print("OPPORTUNITY DISCOVERY ENGINE")
print("OPPORTUNITY SCORING")
print("=" * 70)

print(f"Product pain points: {len(pain_points)}")
print(f"Market categories: {len(market_gaps)}")
print(f"Demand/problem records: {len(demand_problem)}")


# =========================================================
# PREPARE PRODUCT OPPORTUNITIES
# =========================================================

opportunities = pain_points[
    [
        "product_id",
        "product_name",
        "category",
        "subcategory",
        "complaint_category",
        "complaint_count",
        "product_pain_score",
        "demand_problem_score"
    ]
].copy()


# =========================================================
# ADD MARKET GAP INFORMATION
# =========================================================

opportunities = opportunities.merge(
    market_gaps[
        [
            "category",
            "market_gap_score",
            "market_gap_level"
        ]
    ],
    on="category",
    how="left"
)


# =========================================================
# HANDLE MISSING VALUES
# =========================================================

opportunities["market_gap_score"] = (
    opportunities["market_gap_score"]
    .fillna(0)
)

opportunities["product_pain_score"] = (
    opportunities["product_pain_score"]
    .fillna(0)
)

opportunities["demand_problem_score"] = (
    opportunities["demand_problem_score"]
    .fillna(0)
)


# =========================================================
# OPPORTUNITY SCORE
# =========================================================
#
# Customer pain       = 35%
# Demand + problems   = 35%
# Market gap          = 30%
#
# =========================================================

opportunities["opportunity_score"] = (
    0.35 * opportunities["product_pain_score"]
    + 0.35 * opportunities["demand_problem_score"]
    + 0.30 * opportunities["market_gap_score"]
)


# =========================================================
# OPPORTUNITY LEVEL
# =========================================================

def classify_opportunity(score):

    if score >= 75:
        return "High Priority Opportunity"

    elif score >= 50:
        return "Strong Opportunity"

    elif score >= 25:
        return "Moderate Opportunity"

    else:
        return "Low Priority Opportunity"


opportunities["opportunity_level"] = (
    opportunities["opportunity_score"]
    .apply(classify_opportunity)
)


# =========================================================
# OPPORTUNITY DESCRIPTION
# =========================================================

opportunities["opportunity_statement"] = (
    "Improve "
    + opportunities["category"].astype(str)
    + " products by addressing "
    + opportunities["complaint_category"].astype(str)
    + " problems"
)


# =========================================================
# ROUND SCORES
# =========================================================

score_columns = [
    "product_pain_score",
    "demand_problem_score",
    "market_gap_score",
    "opportunity_score"
]

for column in score_columns:

    opportunities[column] = (
        opportunities[column]
        .round(2)
    )


# =========================================================
# RANK OPPORTUNITIES
# =========================================================

opportunities = opportunities.sort_values(
    "opportunity_score",
    ascending=False
)

opportunities["opportunity_rank"] = (
    range(1, len(opportunities) + 1)
)


# =========================================================
# SAVE RESULT
# =========================================================

output_file = (
    FEATURES_DIR /
    "innovation_opportunities.csv"
)

opportunities.to_csv(
    output_file,
    index=False
)


# =========================================================
# DISPLAY TOP OPPORTUNITIES
# =========================================================

print("\n")
print("=" * 70)
print("TOP INNOVATION OPPORTUNITIES")
print("=" * 70)

print(
    opportunities[
        [
            "opportunity_rank",
            "product_name",
            "category",
            "complaint_category",
            "product_pain_score",
            "demand_problem_score",
            "market_gap_score",
            "opportunity_score",
            "opportunity_level"
        ]
    ]
    .head(15)
    .to_string(index=False)
)


# =========================================================
# OPPORTUNITY DISTRIBUTION
# =========================================================

print("\n")
print("=" * 70)
print("OPPORTUNITY LEVEL DISTRIBUTION")
print("=" * 70)

print(
    opportunities[
        "opportunity_level"
    ]
    .value_counts()
    .to_string()
)


# =========================================================
# STRONGEST OPPORTUNITY
# =========================================================

top_opportunity = opportunities.iloc[0]

print("\n")
print("=" * 70)
print("STRONGEST INNOVATION OPPORTUNITY")
print("=" * 70)

print(
    f"Product: "
    f"{top_opportunity['product_name']}"
)

print(
    f"Category: "
    f"{top_opportunity['category']}"
)

print(
    f"Customer problem: "
    f"{top_opportunity['complaint_category']}"
)

print(
    f"Opportunity score: "
    f"{top_opportunity['opportunity_score']}"
)

print(
    f"Priority: "
    f"{top_opportunity['opportunity_level']}"
)

print(
    f"Statement: "
    f"{top_opportunity['opportunity_statement']}"
)


# =========================================================
# FINAL OUTPUT
# =========================================================

print("\n")
print("=" * 70)
print("OPPORTUNITY SCORING COMPLETE")
print("=" * 70)

print(
    f"Total opportunities: {len(opportunities)}"
)

print(
    f"Saved to: {output_file}"
)