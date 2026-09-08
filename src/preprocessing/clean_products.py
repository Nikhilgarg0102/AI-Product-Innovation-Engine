import pandas as pd
from pathlib import Path


# -----------------------------------
# 1. Project paths
# -----------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "company"
    / "products.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

OUTPUT_FILE = OUTPUT_DIR / "products_clean.csv"


# -----------------------------------
# 2. Load raw data
# -----------------------------------

df = pd.read_csv(INPUT_FILE)

print("Raw products dataset loaded.")
print(f"Rows: {len(df)}")


# -----------------------------------
# 3. Clean column names
# -----------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)


# -----------------------------------
# 4. Remove duplicate products
# -----------------------------------

before = len(df)

df = df.drop_duplicates(
    subset=["product_id"]
)

after = len(df)

print(
    f"Duplicates removed: "
    f"{before - after}"
)


# -----------------------------------
# 5. Clean text columns
# -----------------------------------

text_columns = [
    "product_name",
    "category",
    "description"
]

for column in text_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
        )


# -----------------------------------
# 6. Clean price
# -----------------------------------

if "price" in df.columns:

    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    )

    # Remove invalid prices
    df = df[
        df["price"] > 0
    ]


# -----------------------------------
# 7. Clean rating
# -----------------------------------

if "rating" in df.columns:

    df["rating"] = pd.to_numeric(
        df["rating"],
        errors="coerce"
    )

    # Keep ratings between 0 and 5
    df["rating"] = df["rating"].clip(
        lower=0,
        upper=5
    )


# -----------------------------------
# 8. Sort products
# -----------------------------------

if "product_id" in df.columns:

    df = df.sort_values(
        "product_id"
    )


# -----------------------------------
# 9. Create processed directory
# -----------------------------------

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# -----------------------------------
# 10. Save clean dataset
# -----------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# -----------------------------------
# 11. Final verification
# -----------------------------------

print("\nProducts cleaned successfully!")

print(f"Output: {OUTPUT_FILE}")

print(f"Final rows: {len(df)}")

print("\nColumns:")

print(df.columns.tolist())

print("\nMissing values:")

print(df.isnull().sum())

print("\nFirst 5 products:")

print(df.head())