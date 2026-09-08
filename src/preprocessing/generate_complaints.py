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

PRODUCTS_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "company"
    / "products.csv"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "customers"
    / "complaints.csv"
)


# -----------------------------------
# 2. Load datasets
# -----------------------------------

customers = pd.read_csv(CUSTOMERS_FILE)
products = pd.read_csv(PRODUCTS_FILE)


# -----------------------------------
# 3. Complaint templates
# -----------------------------------

complaints = {
    "battery": [
        "Battery life is much lower than expected.",
        "The battery drains very quickly.",
        "I have to charge the product too frequently.",
        "Battery performance has become poor."
    ],

    "quality": [
        "The product quality is disappointing.",
        "The product does not feel durable.",
        "The product stopped working properly after a short time.",
        "The build quality could be much better."
    ],

    "price": [
        "The product is too expensive for its quality.",
        "The price does not seem justified.",
        "I expected better quality at this price."
    ],

    "performance": [
        "The product performance is not as expected.",
        "The product is slow and sometimes stops responding.",
        "The performance has become inconsistent.",
        "The product does not work reliably."
    ],

    "comfort": [
        "The product is uncomfortable during long use.",
        "The design causes discomfort after extended use.",
        "The product needs a more comfortable design."
    ],

    "software": [
        "The software has several problems.",
        "The application frequently crashes.",
        "The software is difficult to use.",
        "The product software needs improvement."
    ],

    "delivery": [
        "The product was delivered later than expected.",
        "My order arrived late.",
        "The delivery process was disappointing."
    ]
}


# -----------------------------------
# 4. Generate complaints
# -----------------------------------

random.seed(42)

complaint_records = []

complaint_categories = list(complaints.keys())

for i in range(1, 50001):

    # Select customer
    customer = customers.sample(
        n=1,
        random_state=random.randint(1, 1000000)
    ).iloc[0]

    customer_id = customer["customer_id"]
    company_id = customer["company_id"]

    # Select product from same company
    company_products = products[
        products["company_id"] == company_id
    ]

    product = company_products.sample(
        n=1,
        random_state=random.randint(1, 1000000)
    ).iloc[0]

    product_id = product["product_id"]

    # Select complaint category
    category = random.choices(
        complaint_categories,
        weights=[25, 20, 10, 15, 10, 10, 10],
        k=1
    )[0]

    complaint_text = random.choice(
        complaints[category]
    )

    complaint_date = (
        datetime(2023, 1, 1)
        + timedelta(days=random.randint(0, 1095))
    ).strftime("%Y-%m-%d")

    priority = random.choices(
        ["Low", "Medium", "High", "Critical"],
        weights=[20, 45, 30, 5],
        k=1
    )[0]

    status = random.choices(
        ["Open", "In Progress", "Resolved", "Closed"],
        weights=[10, 15, 50, 25],
        k=1
    )[0]

    complaint_records.append({
        "complaint_id": f"CMP{i:06d}",
        "company_id": company_id,
        "product_id": product_id,
        "customer_id": customer_id,
        "complaint_category": category,
        "complaint_text": complaint_text,
        "priority": priority,
        "status": status,
        "complaint_date": complaint_date
    })


# -----------------------------------
# 5. Convert to DataFrame
# -----------------------------------

df = pd.DataFrame(complaint_records)


# -----------------------------------
# 6. Save
# -----------------------------------

df.to_csv(OUTPUT_FILE, index=False)


# -----------------------------------
# 7. Verification
# -----------------------------------

print("Complaints dataset created successfully!")
print(f"Location: {OUTPUT_FILE}")
print(f"Number of complaints: {len(df)}")
print(f"Unique customers: {df['customer_id'].nunique()}")
print(f"Unique products: {df['product_id'].nunique()}")

print("\nComplaint categories:")
print(df["complaint_category"].value_counts())

print("\nPriority distribution:")
print(df["priority"].value_counts())

print("\nStatus distribution:")
print(df["status"].value_counts())