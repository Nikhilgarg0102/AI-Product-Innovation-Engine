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

competitors = pd.read_csv(
    PROCESSED_DIR / "competitors_clean.csv"
)

pain_points = pd.read_csv(
    FEATURES_DIR / "pain_point_analysis.csv"
)

demand_problem = pd.read_csv(
    FEATURES_DIR / "product_demand_problem.csv"
)


print("=" * 70)
print("OPPORTUNITY DISCOVERY ENGINE")
print("MARKET GAP ANALYSIS")
print("=" * 70)

print(f"Competitor records: {len(competitors)}")
print(f"Pain point records: {len(pain_points)}")
print(f"Product opportunity records: {len(demand_problem)}")


# =========================================================
# MARKET CATEGORY ANALYSIS
# =========================================================

market_analysis = (
    competitors
    .groupby("category")
    .agg(
        competitor_count=("competitor_id", "nunique"),
        average_price=("competitor_price", "mean"),
        average_feature_count=("feature_count", "mean"),
        average_rating=("market_rating", "mean"),
        average_market_share=(
            "estimated_market_share",
            "mean"
        ),
        average_trend_score=("trend_score", "mean")
    )
    .reset_index()
)


# =========================================================
# FEATURE COVERAGE SCORE
# =========================================================

max_features = (
    market_analysis["average_feature_count"].max()
)

if max_features > 0:

    market_analysis["feature_coverage_score"] = (
        market_analysis["average_feature_count"]
        / max_features
    ) * 100

else:

    market_analysis["feature_coverage_score"] = 0


# =========================================================
# MARKET OPPORTUNITY SCORE
# =========================================================

max_trend = (
    market_analysis["average_trend_score"].max()
)

if max_trend > 0:

    market_analysis["market_trend_score"] = (
        market_analysis["average_trend_score"]
        / max_trend
    ) * 100

else:

    market_analysis["market_trend_score"] = 0


# =========================================================
# COMPETITOR DENSITY
# =========================================================

max_competitors = (
    market_analysis["competitor_count"].max()
)

if max_competitors > 0:

    market_analysis["competition_score"] = (
        market_analysis["competitor_count"]
        / max_competitors
    ) * 100

else:

    market_analysis["competition_score"] = 0


# =========================================================
# GAP SCORE
# =========================================================
#
# Lower feature coverage + higher market trend
# = stronger potential market gap.
#
# =========================================================

market_analysis["feature_gap_score"] = (
    100 -
    market_analysis["feature_coverage_score"]
)


market_analysis["market_gap_score"] = (
    0.50 * market_analysis["feature_gap_score"]
    + 0.35 * market_analysis["market_trend_score"]
    + 0.15 * (
        100 -
        market_analysis["competition_score"]
    )
)


# =========================================================
# GAP CLASSIFICATION
# =========================================================

def classify_gap(score):

    if score >= 75:
        return "Critical Market Gap"

    elif score >= 50:
        return "High Market Gap"

    elif score >= 25:
        return "Moderate Market Gap"

    else:
        return "Low Market Gap"


market_analysis["market_gap_level"] = (
    market_analysis["market_gap_score"]
    .apply(classify_gap)
)


# =========================================================
# ROUND VALUES
# =========================================================

numeric_columns = [
    "average_price",
    "average_feature_count",
    "average_rating",
    "average_market_share",
    "average_trend_score",
    "feature_coverage_score",
    "market_trend_score",
    "competition_score",
    "feature_gap_score",
    "market_gap_score"
]

for column in numeric_columns:

    market_analysis[column] = (
        market_analysis[column]
        .round(2)
    )


# =========================================================
# SORT MARKET GAPS
# =========================================================

market_analysis = (
    market_analysis
    .sort_values(
        "market_gap_score",
        ascending=False
    )
)


# =========================================================
# SAVE MARKET GAP ANALYSIS
# =========================================================

output_file = (
    FEATURES_DIR /
    "market_gap_analysis.csv"
)

market_analysis.to_csv(
    output_file,
    index=False
)


# =========================================================
# DISPLAY MARKET GAPS
# =========================================================

print("\n")
print("=" * 70)
print("TOP MARKET GAPS")
print("=" * 70)

print(
    market_analysis[
        [
            "category",
            "competitor_count",
            "average_feature_count",
            "average_trend_score",
            "feature_gap_score",
            "market_gap_score",
            "market_gap_level"
        ]
    ]
    .to_string(index=False)
)


# =========================================================
# COMBINE PAIN POINTS WITH MARKET GAPS
# =========================================================

top_pain_point = (
    pain_points
    .sort_values(
        "pain_point_score",
        ascending=False
    )
    .iloc[0]
)


top_pain_category = (
    top_pain_point["complaint_category"]
)

top_pain_score = (
    top_pain_point["pain_point_score"]
)


# =========================================================
# GLOBAL INNOVATION SIGNAL
# =========================================================

top_market_gap = (
    market_analysis
    .iloc[0]
)


print("\n")
print("=" * 70)
print("STRONGEST INNOVATION SIGNAL")
print("=" * 70)

print(
    f"Top customer pain point: "
    f"{top_pain_category}"
)

print(
    f"Pain point score: "
    f"{top_pain_score}"
)

print(
    f"Top market gap category: "
    f"{top_market_gap['category']}"
)

print(
    f"Market gap score: "
    f"{top_market_gap['market_gap_score']}"
)


# =========================================================
# FINAL OUTPUT
# =========================================================

print("\n")
print("=" * 70)
print("MARKET GAP ANALYSIS COMPLETE")
print("=" * 70)

print(
    f"Saved to: {output_file}"
)