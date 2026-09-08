import pandas as pd
from pathlib import Path
import random
from datetime import datetime, timedelta


# -----------------------------------
# 1. Project paths
# -----------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CUSTOMERS_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "customers"
    / "customers.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "customers"
    / "surveys.csv"
)


# -----------------------------------
# 2. Load customers
# -----------------------------------

customers = pd.read_csv(CUSTOMERS_FILE)


# -----------------------------------
# 3. Survey questions and answers
# -----------------------------------

feature_preferences = [
    "Longer battery life",
    "Better performance",
    "Improved comfort",
    "Better design",
    "Lower price",
    "More smart features",
    "Better software",
    "Improved durability"
]

purchase_factors = [
    "Price",
    "Quality",
    "Brand reputation",
    "Features",
    "Design",
    "Performance",
    "Durability",
    "Customer reviews"
]

improvement_areas = [
    "Battery life",
    "Performance",
    "Design",
    "Comfort",
    "Software",
    "Price",
    "Durability",
    "Customer support"
]


# -----------------------------------
# 4. Generate surveys
# -----------------------------------

random.seed(42)

survey_records = []

for i in range(1, 30001):

    # Select customer
    customer = customers.sample(
        n=1,
        random_state=random.randint(1, 1000000)
    ).iloc[0]

    customer_id = customer["customer_id"]
    company_id = customer["company_id"]

    survey_date = (
        datetime(2023, 1, 1)
        + timedelta(days=random.randint(0, 1095))
    ).strftime("%Y-%m-%d")

    satisfaction_score = random.randint(1, 10)

    recommended = (
        "Yes"
        if satisfaction_score >= 7
        else "No"
    )

    survey_records.append({
        "survey_id": f"SRV{i:06d}",
        "company_id": company_id,
        "customer_id": customer_id,
        "survey_date": survey_date,
        "satisfaction_score": satisfaction_score,
        "preferred_feature": random.choice(feature_preferences),
        "purchase_factor": random.choice(purchase_factors),
        "improvement_area": random.choice(improvement_areas),
        "would_recommend": recommended
    })


# -----------------------------------
# 5. Convert to DataFrame
# -----------------------------------

df = pd.DataFrame(survey_records)


# -----------------------------------
# 6. Save
# -----------------------------------

df.to_csv(OUTPUT_FILE, index=False)


# -----------------------------------
# 7. Verification
# -----------------------------------

print("Surveys dataset created successfully!")
print(f"Location: {OUTPUT_FILE}")
print(f"Number of surveys: {len(df)}")
print(f"Unique customers: {df['customer_id'].nunique()}")

print("\nPreferred features:")
print(df["preferred_feature"].value_counts())

print("\nImprovement areas:")
print(df["improvement_area"].value_counts())

print("\nAverage satisfaction score:")
print(f"{df['satisfaction_score'].mean():.2f}/10")