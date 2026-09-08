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
    / "purchases.csv"
)


# -----------------------------------
# 2. Load existing datasets
# -----------------------------------

customers = pd.read_csv(CUSTOMERS_FILE)

products = pd.read_csv(PRODUCTS_FILE)


# -----------------------------------
# 3. Generate purchases
# -----------------------------------

random.seed(42)

purchases = []

for i in range(1, 100001):

    # Select a customer
    customer = customers.sample(
        n=1,
        random_state=random.randint(1, 1000000)
    ).iloc[0]

    customer_id = customer["customer_id"]

    company_id = customer["company_id"]

    # Select products belonging to the same company
    company_products = products[
        products["company_id"] == company_id
    ]

    product = company_products.sample(
        n=1,
        random_state=random.randint(1, 1000000)
    ).iloc[0]

    product_id = product["product_id"]

    original_price = float(product["price"])

    quantity = random.randint(1, 3)

    discount = round(
        random.choice([0, 0.05, 0.10, 0.15, 0.20]),
        2
    )

    unit_price = round(
        original_price * (1 - discount),
        2
    )

    purchase_date = (
        datetime(2023, 1, 1)
        + timedelta(days=random.randint(0, 1095))
    ).strftime("%Y-%m-%d")

    channel = random.choice(
        ["Online", "Retail Store", "Marketplace"]
    )

    region = random.choice(
        [
            "North",
            "South",
            "East",
            "West",
            "Central"
        ]
    )

    purchases.append({
        "purchase_id": f"PUR{i:06d}",
        "company_id": company_id,
        "product_id": product_id,
        "customer_id": customer_id,
        "purchase_date": purchase_date,
        "quantity": quantity,
        "unit_price": unit_price,
        "discount": discount,
        "channel": channel,
        "region": region
    })


# -----------------------------------
# 4. Convert to DataFrame
# -----------------------------------

df = pd.DataFrame(purchases)


# -----------------------------------
# 5. Save
# -----------------------------------

df.to_csv(OUTPUT_FILE, index=False)


# -----------------------------------
# 6. Verification
# -----------------------------------

print("Purchases dataset created successfully!")
print(f"Location: {OUTPUT_FILE}")
print(f"Number of purchases: {len(df)}")
print(f"Unique customers: {df['customer_id'].nunique()}")
print(f"Unique products: {df['product_id'].nunique()}")
print(f"Companies represented: {df['company_id'].nunique()}")