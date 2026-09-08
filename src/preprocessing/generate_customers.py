import pandas as pd
from pathlib import Path
import random
from datetime import datetime, timedelta


# -----------------------------------
# 1. Project paths
# -----------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "customers"
    / "customers.csv"
)


# -----------------------------------
# 2. Possible customer values
# -----------------------------------

age_groups = [
    "18-25",
    "26-35",
    "36-45",
    "46-55",
    "56+"
]

genders = [
    "Male",
    "Female",
    "Other"
]

locations = [
    "India",
    "USA",
    "UK",
    "Germany",
    "Canada",
    "Japan",
    "Singapore",
    "South Korea"
]

income_segments = [
    "Low",
    "Medium",
    "High",
    "Premium"
]

customer_segments = [
    "Budget Buyer",
    "Value Seeker",
    "Young Professional",
    "Premium Customer",
    "Technology Enthusiast"
]

loyalty_levels = [
    "New",
    "Regular",
    "Loyal",
    "VIP"
]


# -----------------------------------
# 3. Generate customers
# -----------------------------------

random.seed(42)

customers = []

for i in range(1, 10001):

    customer_id = f"CUST{i:05d}"

    company_number = random.randint(1, 10)

    company_id = f"C{company_number:03d}"

    registration_date = (
        datetime(2020, 1, 1)
        + timedelta(days=random.randint(0, 2400))
    ).strftime("%Y-%m-%d")

    customers.append({
        "customer_id": customer_id,
        "company_id": company_id,
        "age_group": random.choice(age_groups),
        "gender": random.choice(genders),
        "location": random.choice(locations),
        "income_segment": random.choice(income_segments),
        "customer_segment": random.choice(customer_segments),
        "registration_date": registration_date,
        "loyalty_level": random.choice(loyalty_levels)
    })


# -----------------------------------
# 4. Convert to DataFrame
# -----------------------------------

df = pd.DataFrame(customers)


# -----------------------------------
# 5. Save CSV
# -----------------------------------

df.to_csv(OUTPUT_FILE, index=False)


# -----------------------------------
# 6. Verification
# -----------------------------------

print("Customers dataset created successfully!")
print(f"Location: {OUTPUT_FILE}")
print(f"Number of customers: {len(df)}")
print(f"Companies represented: {df['company_id'].nunique()}")
print(f"Customer segments: {df['customer_segment'].nunique()}")