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
    / "company"
    / "products.csv"
)


# -----------------------------------
# 2. Product categories
# -----------------------------------

categories = {
    "Watches": [
        "Smart Watch",
        "Analog Watch",
        "Fitness Watch"
    ],
    "Audio": [
        "Wireless Earbuds",
        "Headphones",
        "Bluetooth Speaker"
    ],
    "Mobile": [
        "Smartphone",
        "Tablet"
    ],
    "Home Appliances": [
        "Air Purifier",
        "Smart Fan",
        "Smart Light"
    ],
    "Wearables": [
        "Fitness Band",
        "Smart Ring"
    ]
}


# -----------------------------------
# 3. Product generation
# -----------------------------------

products = []

random.seed(42)

product_number = 1

for company_number in range(1, 11):

    company_id = f"C{company_number:03d}"

    # Each company gets 50 products
    for _ in range(50):

        category = random.choice(list(categories.keys()))

        subcategory = random.choice(categories[category])

        product_id = f"P{product_number:04d}"

        product_name = f"{subcategory} {product_number}"

        price = random.randint(1000, 50000)

        cost = round(price * random.uniform(0.45, 0.75), 2)

        rating = round(random.uniform(3.2, 4.9), 1)

        total_sales = random.randint(500, 100000)

        return_rate = round(random.uniform(0.01, 0.15), 3)

        launch_date = (
            datetime(2022, 1, 1)
            + timedelta(days=random.randint(0, 1500))
        ).strftime("%Y-%m-%d")

        lifecycle_stage = random.choice(
            ["Introduction", "Growth", "Mature", "Decline"]
        )

        status = random.choice(
            ["Active", "Active", "Active", "Discontinued"]
        )

        description = (
            f"{subcategory} designed for modern consumers "
            f"with practical features and reliable performance."
        )

        products.append({
            "product_id": product_id,
            "company_id": company_id,
            "product_name": product_name,
            "category": category,
            "subcategory": subcategory,
            "description": description,
            "launch_date": launch_date,
            "price": price,
            "cost": cost,
            "rating": rating,
            "total_sales": total_sales,
            "return_rate": return_rate,
            "lifecycle_stage": lifecycle_stage,
            "status": status
        })

        product_number += 1


# -----------------------------------
# 4. Convert to DataFrame
# -----------------------------------

df = pd.DataFrame(products)


# -----------------------------------
# 5. Save dataset
# -----------------------------------

df.to_csv(OUTPUT_FILE, index=False)


# -----------------------------------
# 6. Verification
# -----------------------------------

print("Products dataset created successfully!")
print(f"Location: {OUTPUT_FILE}")
print(f"Number of products: {len(df)}")
print(f"Number of companies: {df['company_id'].nunique()}")
print(f"Number of categories: {df['category'].nunique()}")