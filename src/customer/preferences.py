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

customers = data["customers"]
surveys = data["surveys"]


# --------------------------------------------------
# Load customer segments
# --------------------------------------------------

segments_file = (
    PROJECT_ROOT
    / "data"
    / "features"
    / "customer_segments.csv"
)

segments = pd.read_csv(segments_file)


print("=" * 65)
print("CUSTOMER INTELLIGENCE ENGINE")
print("CUSTOMER PREFERENCE ANALYSIS")
print("=" * 65)


# --------------------------------------------------
# Connect surveys with customer segments
# --------------------------------------------------

survey_data = surveys.merge(
    segments[
        [
            "customer_id",
            "customer_segment"
        ]
    ],
    on="customer_id",
    how="left"
)


# --------------------------------------------------
# Remove surveys without a segment
# --------------------------------------------------

survey_data = survey_data.dropna(
    subset=["customer_segment"]
)


# --------------------------------------------------
# Preference analysis
# --------------------------------------------------

feature_preferences = (
    survey_data
    .groupby(
        [
            "customer_segment",
            "preferred_feature"
        ]
    )
    .size()
    .reset_index(
        name="request_count"
    )
)


feature_preferences["preference_percentage"] = (
    feature_preferences["request_count"]
    /
    feature_preferences
    .groupby("customer_segment")[
        "request_count"
    ]
    .transform("sum")
    * 100
)


feature_preferences = (
    feature_preferences
    .sort_values(
        [
            "customer_segment",
            "request_count"
        ],
        ascending=[True, False]
    )
)


# --------------------------------------------------
# Improvement analysis
# --------------------------------------------------

improvement_analysis = (
    survey_data
    .groupby(
        [
            "customer_segment",
            "improvement_area"
        ]
    )
    .size()
    .reset_index(
        name="request_count"
    )
)


improvement_analysis["improvement_percentage"] = (
    improvement_analysis["request_count"]
    /
    improvement_analysis
    .groupby("customer_segment")[
        "request_count"
    ]
    .transform("sum")
    * 100
)


improvement_analysis = (
    improvement_analysis
    .sort_values(
        [
            "customer_segment",
            "request_count"
        ],
        ascending=[True, False]
    )
)


# --------------------------------------------------
# Purchase factor analysis
# --------------------------------------------------

purchase_factors = (
    survey_data
    .groupby(
        [
            "customer_segment",
            "purchase_factor"
        ]
    )
    .size()
    .reset_index(
        name="request_count"
    )
)


purchase_factors = (
    purchase_factors
    .sort_values(
        [
            "customer_segment",
            "request_count"
        ],
        ascending=[True, False]
    )
)


# --------------------------------------------------
# Satisfaction analysis
# --------------------------------------------------

satisfaction = (
    survey_data
    .groupby("customer_segment")
    ["satisfaction_score"]
    .mean()
    .reset_index()
)


satisfaction = satisfaction.rename(
    columns={
        "satisfaction_score":
        "average_satisfaction"
    }
)


# --------------------------------------------------
# Save feature datasets
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


feature_preferences.to_csv(
    OUTPUT_DIR
    / "customer_feature_preferences.csv",
    index=False
)


improvement_analysis.to_csv(
    OUTPUT_DIR
    / "customer_improvement_areas.csv",
    index=False
)


purchase_factors.to_csv(
    OUTPUT_DIR
    / "customer_purchase_factors.csv",
    index=False
)


satisfaction.to_csv(
    OUTPUT_DIR
    / "customer_satisfaction.csv",
    index=False
)


# --------------------------------------------------
# Display results
# --------------------------------------------------

print("\nCustomer preference analysis complete.")

print(
    f"Surveys analysed: "
    f"{len(survey_data):,}"
)


print("\nTop requested features:")

print(
    feature_preferences
    .head(15)
)


print("\nTop improvement areas:")

print(
    improvement_analysis
    .head(15)
)


print("\nCustomer satisfaction:")

print(
    satisfaction
)


print("\nOutput files created:")

print(
    "customer_feature_preferences.csv"
)

print(
    "customer_improvement_areas.csv"
)

print(
    "customer_purchase_factors.csv"
)

print(
    "customer_satisfaction.csv"
)


print("\n" + "=" * 65)
print("CUSTOMER PREFERENCE INTELLIGENCE COMPLETE")
print("=" * 65)