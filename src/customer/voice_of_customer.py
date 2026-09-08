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

complaints = data["complaints"]
reviews = data["reviews"]


print("=" * 65)
print("CUSTOMER INTELLIGENCE ENGINE")
print("VOICE OF CUSTOMER ANALYSIS")
print("=" * 65)


# --------------------------------------------------
# 1. Complaint category analysis
# --------------------------------------------------

complaint_categories = (
    complaints
    .groupby("complaint_category")
    .size()
    .reset_index(
        name="complaint_count"
    )
)


complaint_categories["percentage"] = (
    complaint_categories["complaint_count"]
    /
    complaint_categories["complaint_count"].sum()
    * 100
)


complaint_categories = (
    complaint_categories
    .sort_values(
        "complaint_count",
        ascending=False
    )
)


# --------------------------------------------------
# 2. Complaint priority analysis
# --------------------------------------------------

priority_analysis = (
    complaints
    .groupby("priority")
    .size()
    .reset_index(
        name="complaint_count"
    )
    .sort_values(
        "complaint_count",
        ascending=False
    )
)


# --------------------------------------------------
# 3. Complaint status analysis
# --------------------------------------------------

status_analysis = (
    complaints
    .groupby("status")
    .size()
    .reset_index(
        name="complaint_count"
    )
    .sort_values(
        "complaint_count",
        ascending=False
    )
)


# --------------------------------------------------
# 4. Review rating analysis
# --------------------------------------------------

review_ratings = (
    reviews
    .groupby("rating")
    .size()
    .reset_index(
        name="review_count"
    )
    .sort_values(
        "rating"
    )
)


# --------------------------------------------------
# 5. Average rating
# --------------------------------------------------

average_rating = reviews["rating"].mean()


# --------------------------------------------------
# 6. Complaint category by company
# --------------------------------------------------

company_complaints = (
    complaints
    .groupby(
        [
            "company_id",
            "complaint_category"
        ]
    )
    .size()
    .reset_index(
        name="complaint_count"
    )
)


company_complaints = (
    company_complaints
    .sort_values(
        "complaint_count",
        ascending=False
    )
)


# --------------------------------------------------
# 7. Complaint category by product
# --------------------------------------------------

product_complaints = (
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


product_complaints = (
    product_complaints
    .sort_values(
        "complaint_count",
        ascending=False
    )
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


complaint_categories.to_csv(
    OUTPUT_DIR
    / "complaint_category_analysis.csv",
    index=False
)


priority_analysis.to_csv(
    OUTPUT_DIR
    / "complaint_priority_analysis.csv",
    index=False
)


status_analysis.to_csv(
    OUTPUT_DIR
    / "complaint_status_analysis.csv",
    index=False
)


review_ratings.to_csv(
    OUTPUT_DIR
    / "review_rating_analysis.csv",
    index=False
)


company_complaints.to_csv(
    OUTPUT_DIR
    / "company_complaints.csv",
    index=False
)


product_complaints.to_csv(
    OUTPUT_DIR
    / "product_complaints.csv",
    index=False
)


# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\nComplaint categories:")

print(
    complaint_categories
)


print("\nComplaint priorities:")

print(
    priority_analysis
)


print("\nComplaint statuses:")

print(
    status_analysis
)


print(
    f"\nAverage review rating: "
    f"{average_rating:.2f}"
)


print("\nReview rating distribution:")

print(
    review_ratings
)


print("\nTop company complaint patterns:")

print(
    company_complaints.head(10)
)


print("\nTop product complaint patterns:")

print(
    product_complaints.head(10)
)


print("\n" + "=" * 65)
print("VOICE OF CUSTOMER ANALYSIS COMPLETE")
print("=" * 65)