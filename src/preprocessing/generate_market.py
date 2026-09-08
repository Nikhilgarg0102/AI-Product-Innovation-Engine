import pandas as pd
from pathlib import Path
import random


# -----------------------------------
# 1. Project paths
# -----------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

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
    / "market"
    / "competitors.csv"
)


# -----------------------------------
# 2. Load products
# -----------------------------------

products = pd.read_csv(PRODUCTS_FILE)


# -----------------------------------
# 3. Competitor information
# -----------------------------------

competitor_names = [
    "Competitor_A",
    "Competitor_B",
    "Competitor_C",
    "Competitor_D",
    "Competitor_E"
]

market_regions = [
    "India",
    "USA",
    "UK",
    "Germany",
    "Japan",
    "Canada"
]

market_channels = [
    "Online",
    "Retail",
    "Marketplace"
]


# -----------------------------------
# 4. Generate competitor data
# -----------------------------------

random.seed(42)

records = []

for i in range(1, 20001):

    product = products.sample(
        n=1,
        random_state=random.randint(1, 1000000)
    ).iloc[0]

    category = product["category"]

    base_price = float(product["price"])

    competitor = random.choice(
        competitor_names
    )

    # Competitor price variation
    price_multiplier = random.uniform(
        0.75,
        1.35
    )

    competitor_price = round(
        base_price * price_multiplier,
        2
    )

    feature_count = random.randint(
        3,
        12
    )

    market_rating = round(
        random.uniform(3.0, 5.0),
        1
    )

    estimated_market_share = round(
        random.uniform(2, 25),
        2
    )

    trend_score = round(
        random.uniform(20, 100),
        2
    )

    records.append({
        "competitor_id": f"COMP{i:05d}",
        "competitor_name": competitor,
        "category": category,
        "competitor_price": competitor_price,
        "feature_count": feature_count,
        "market_rating": market_rating,
        "estimated_market_share": estimated_market_share,
        "trend_score": trend_score,
        "market_region": random.choice(market_regions),
        "sales_channel": random.choice(market_channels)
    })


# -----------------------------------
# 5. Create DataFrame
# -----------------------------------

df = pd.DataFrame(records)


# -----------------------------------
# 6. Save dataset
# -----------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# -----------------------------------
# 7. Verification
# -----------------------------------

print("Market dataset created successfully!")

print(f"Location: {OUTPUT_FILE}")

print(f"Number of records: {len(df)}")

print(
    f"Competitors: "
    f"{df['competitor_name'].nunique()}"
)

print(
    f"Categories: "
    f"{df['category'].nunique()}"
)

print(
    f"Average competitor price: "
    f"{df['competitor_price'].mean():.2f}"
)

print(
    f"Average market rating: "
    f"{df['market_rating'].mean():.2f}"
)