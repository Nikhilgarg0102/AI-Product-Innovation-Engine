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
    / "customers"
    / "purchases.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

OUTPUT_FILE = OUTPUT_DIR / "purchases_clean.csv"


# -----------------------------------
# 2. Load dataset
# -----------------------------------

df = pd.read_csv(INPUT_FILE)

print("Raw purchases dataset loaded.")
print(f"Rows before cleaning: {len(df)}")


# -----------------------------------
# 3. Standardize column names
# -----------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)


# -----------------------------------
# 4. Remove duplicate purchases
# -----------------------------------

before = len(df)

df = df.drop_duplicates(
    subset=["purchase_id"]
)

duplicates_removed = before - len(df)

print(
    f"Duplicate purchases removed: "
    f"{duplicates_removed}"
)


# -----------------------------------
# 5. Clean text columns
# -----------------------------------

text_columns = [
    "purchase_id",
    "company_id",
    "product_id",
    "customer_id",
    "channel",
    "region"
]

for column in text_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
        )


# -----------------------------------
# 6. Convert purchase date
# -----------------------------------

if "purchase_date" in df.columns:

    df["purchase_date"] = pd.to_datetime(
        df["purchase_date"],
        errors="coerce"
    )


# -----------------------------------
# 7. Clean quantity
# -----------------------------------

if "quantity" in df.columns:

    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    )

    # Quantity must be positive
    df.loc[
        df["quantity"] <= 0,
        "quantity"
    ] = pd.NA


# -----------------------------------
# 8. Clean unit price
# -----------------------------------

if "unit_price" in df.columns:

    df["unit_price"] = pd.to_numeric(
        df["unit_price"],
        errors="coerce"
    )

    # Price must be positive
    df.loc[
        df["unit_price"] <= 0,
        "unit_price"
    ] = pd.NA


# -----------------------------------
# 9. Clean discount
# -----------------------------------

if "discount" in df.columns:

    df["discount"] = pd.to_numeric(
        df["discount"],
        errors="coerce"
    )

    # Keep discount between 0 and 100
    df["discount"] = df["discount"].clip(
        lower=0,
        upper=100
    )


# -----------------------------------
# 10. Remove rows without key IDs
# -----------------------------------

key_columns = [
    "purchase_id",
    "company_id",
    "product_id",
    "customer_id"
]

df = df.dropna(
    subset=key_columns
)


# -----------------------------------
# 11. Remove invalid transactions
# -----------------------------------

required_numeric = [
    "quantity",
    "unit_price"
]

df = df.dropna(
    subset=required_numeric
)


# -----------------------------------
# 12. Sort by purchase date
# -----------------------------------

if "purchase_date" in df.columns:

    df = df.sort_values(
        "purchase_date"
    )


# -----------------------------------
# 13. Create processed directory
# -----------------------------------

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# -----------------------------------
# 14. Save cleaned dataset
# -----------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# -----------------------------------
# 15. Final verification
# -----------------------------------

print("\n" + "=" * 55)

print("PURCHASE CLEANING COMPLETE")

print("=" * 55)

print(
    f"Rows after cleaning: {len(df)}"
)

print(
    f"Rows removed: "
    f"{before - len(df)}"
)

print(
    f"Output: {OUTPUT_FILE}"
)

print("\nMissing values:")

print(df.isnull().sum())

print("\nNumeric summary:")

print(
    df[
        [
            "quantity",
            "unit_price",
            "discount"
        ]
    ].describe()
)

print("\nFirst 5 purchases:")

print(df.head())