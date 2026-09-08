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
reviews = data["reviews"]


print("=" * 70)
print("PRODUCT INTELLIGENCE ENGINE")
print("PRODUCT REVIEW ANALYSIS")
print("=" * 70)


# --------------------------------------------------
# 1. Create sentiment from rating
# --------------------------------------------------

def classify_sentiment(rating):

    if rating >= 4:
        return "Positive"

    elif rating == 3:
        return "Neutral"

    else:
        return "Negative"


reviews["sentiment"] = (
    reviews["rating"]
    .apply(classify_sentiment)
)


# --------------------------------------------------
# 2. Product review statistics
# --------------------------------------------------

review_stats = (
    reviews
    .groupby("product_id")
    .agg(
        review_count=("rating", "count"),
        average_rating=("rating", "mean")
    )
    .reset_index()
)


# --------------------------------------------------
# 3. Sentiment counts
# --------------------------------------------------

sentiment_counts = (
    reviews
    .groupby(
        [
            "product_id",
            "sentiment"
        ]
    )
    .size()
    .reset_index(
        name="count"
    )
)


# --------------------------------------------------
# 4. Convert sentiment into columns
# --------------------------------------------------

sentiment_pivot = (
    sentiment_counts
    .pivot(
        index="product_id",
        columns="sentiment",
        values="count"
    )
    .fillna(0)
    .reset_index()
)


# --------------------------------------------------
# 5. Make sure all sentiment columns exist
# --------------------------------------------------

for column in [
    "Positive",
    "Neutral",
    "Negative"
]:

    if column not in sentiment_pivot.columns:
        sentiment_pivot[column] = 0


# --------------------------------------------------
# 6. Merge statistics
# --------------------------------------------------

review_analysis = review_stats.merge(
    sentiment_pivot,
    on="product_id",
    how="left"
)


# --------------------------------------------------
# 7. Calculate percentages
# --------------------------------------------------

review_analysis["positive_percentage"] = (
    review_analysis["Positive"]
    /
    review_analysis["review_count"]
    * 100
)


review_analysis["neutral_percentage"] = (
    review_analysis["Neutral"]
    /
    review_analysis["review_count"]
    * 100
)


review_analysis["negative_percentage"] = (
    review_analysis["Negative"]
    /
    review_analysis["review_count"]
    * 100
)


# --------------------------------------------------
# 8. Calculate review health score
# --------------------------------------------------

review_analysis["review_health_score"] = (
    review_analysis["positive_percentage"]
    -
    review_analysis["negative_percentage"]
)


# --------------------------------------------------
# 9. Round values
# --------------------------------------------------

review_analysis["average_rating"] = (
    review_analysis["average_rating"]
    .round(2)
)


review_analysis[
    [
        "positive_percentage",
        "neutral_percentage",
        "negative_percentage",
        "review_health_score"
    ]
] = (
    review_analysis[
        [
            "positive_percentage",
            "neutral_percentage",
            "negative_percentage",
            "review_health_score"
        ]
    ]
    .round(2)
)


# --------------------------------------------------
# 10. Add product information
# --------------------------------------------------

review_analysis = review_analysis.merge(
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
# 11. Product review category
# --------------------------------------------------

def review_category(score):

    if score >= 60:
        return "Excellent"

    elif score >= 30:
        return "Good"

    elif score >= 0:
        return "Mixed"

    else:
        return "Poor"


review_analysis["review_category"] = (
    review_analysis["review_health_score"]
    .apply(review_category)
)


# --------------------------------------------------
# 12. Sort products
# --------------------------------------------------

review_analysis = (
    review_analysis
    .sort_values(
        "average_rating",
        ascending=False
    )
)


# --------------------------------------------------
# 13. Save output
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
    / "product_review_analysis.csv"
)


review_analysis.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# 14. Display results
# --------------------------------------------------

print("\nReview analysis complete.")

print(
    f"Reviews analysed: "
    f"{len(reviews):,}"
)


print(
    f"Products analysed: "
    f"{review_analysis['product_id'].nunique():,}"
)


# --------------------------------------------------
# Top-rated products
# --------------------------------------------------

print("\nTop-rated products:")

print(
    review_analysis[
        [
            "product_id",
            "product_name",
            "average_rating",
            "review_count",
            "positive_percentage",
            "negative_percentage",
            "review_health_score",
            "review_category"
        ]
    ]
    .head(10)
)


# --------------------------------------------------
# Weakest review health
# --------------------------------------------------

print("\nProducts with weakest review health:")

weakest_reviews = (
    review_analysis
    .sort_values(
        "review_health_score",
        ascending=True
    )
    .head(10)
)


print(
    weakest_reviews[
        [
            "product_id",
            "product_name",
            "category",
            "average_rating",
            "review_count",
            "positive_percentage",
            "negative_percentage",
            "review_health_score",
            "review_category"
        ]
    ]
)


# --------------------------------------------------
# Review category distribution
# --------------------------------------------------

print("\nReview category distribution:")

print(
    review_analysis[
        "review_category"
    ]
    .value_counts()
)


# --------------------------------------------------
# Overall average rating
# --------------------------------------------------

overall_rating = reviews["rating"].mean()

print(
    f"\nOverall average rating: "
    f"{overall_rating:.2f}"
)


# --------------------------------------------------
# Output
# --------------------------------------------------

print("\nOutput:")

print(
    OUTPUT_FILE
)


print("\n" + "=" * 70)
print("PRODUCT REVIEW ANALYSIS COMPLETE")
print("=" * 70)