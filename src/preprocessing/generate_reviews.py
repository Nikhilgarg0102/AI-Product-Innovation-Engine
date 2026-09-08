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
    / "reviews.csv"
)


# -----------------------------------
# 2. Load datasets
# -----------------------------------

customers = pd.read_csv(CUSTOMERS_FILE)

products = pd.read_csv(PRODUCTS_FILE)


# -----------------------------------
# 3. Review templates
# -----------------------------------

positive_reviews = [
    "I really like this product. The design is excellent.",
    "Very good quality and easy to use.",
    "The product works perfectly and looks premium.",
    "Excellent value for the price.",
    "I am very satisfied with the performance.",
    "The design is attractive and the product feels durable."
]

neutral_reviews = [
    "The product is okay and works as expected.",
    "Overall it is a decent product.",
    "The quality is acceptable for the price.",
    "It performs reasonably well.",
    "Nothing special, but it gets the job done."
]

negative_reviews = [
    "The battery life is disappointing.",
    "The product feels too expensive for its quality.",
    "The quality could be much better.",
    "I experienced several problems while using it.",
    "The product is uncomfortable after long use.",
    "The performance is not as good as expected."
]

mixed_reviews = [
    "The design is excellent but the battery life is poor.",
    "Good performance, but the price is too high.",
    "The product looks great but it could be more comfortable.",
    "The quality is good, although the software needs improvement.",
    "I like the features but the battery could last longer."
]


# -----------------------------------
# 4. Generate reviews
# -----------------------------------

random.seed(42)

reviews = []

for i in range(1, 50001):

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

    review_type = random.choices(
        [
            "positive",
            "neutral",
            "negative",
            "mixed"
        ],
        weights=[45, 20, 15, 20],
        k=1
    )[0]

    if review_type == "positive":
        review_text = random.choice(positive_reviews)
        rating = random.randint(4, 5)

    elif review_type == "neutral":
        review_text = random.choice(neutral_reviews)
        rating = 3

    elif review_type == "negative":
        review_text = random.choice(negative_reviews)
        rating = random.randint(1, 2)

    else:
        review_text = random.choice(mixed_reviews)
        rating = random.randint(2, 4)

    review_date = (
        datetime(2023, 1, 1)
        + timedelta(days=random.randint(0, 1095))
    ).strftime("%Y-%m-%d")

    verified_purchase = random.choice(
        [True, True, True, False]
    )

    reviews.append({
        "review_id": f"REV{i:06d}",
        "company_id": company_id,
        "product_id": product_id,
        "customer_id": customer_id,
        "review_text": review_text,
        "rating": rating,
        "review_date": review_date,
        "verified_purchase": verified_purchase
    })


# -----------------------------------
# 5. Convert to DataFrame
# -----------------------------------

df = pd.DataFrame(reviews)


# -----------------------------------
# 6. Save
# -----------------------------------

df.to_csv(OUTPUT_FILE, index=False)


# -----------------------------------
# 7. Verification
# -----------------------------------

print("Reviews dataset created successfully!")
print(f"Location: {OUTPUT_FILE}")
print(f"Number of reviews: {len(df)}")
print(f"Unique customers: {df['customer_id'].nunique()}")
print(f"Unique products: {df['product_id'].nunique()}")
print(f"Average rating: {df['rating'].mean():.2f}")