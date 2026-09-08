import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "market" / "competitors.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "competitors_clean.csv"


# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("Raw competitor dataset loaded.")
print(f"Rows before cleaning: {len(df)}")


# --------------------------------------------------
# 2. Standardize column names
# --------------------------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)


# --------------------------------------------------
# 3. Remove duplicate competitor records
# --------------------------------------------------

before = len(df)

df = df.drop_duplicates()

duplicates_removed = before - len(df)

print(f"Duplicate records removed: {duplicates_removed}")


# --------------------------------------------------
# 4. Clean text columns
# --------------------------------------------------

text_columns = [
    "competitor_id",
    "competitor_name",
    "category",
    "market_region",
    "sales_channel"
]

for column in text_columns:
    if column in df.columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )


# --------------------------------------------------
# 5. Normalize text
# --------------------------------------------------

if "competitor_name" in df.columns:
    df["competitor_name"] = (
        df["competitor_name"]
        .str.replace(r"\s+", " ", regex=True)
    )

if "category" in df.columns:
    df["category"] = (
        df["category"]
        .str.strip()
        .str.title()
    )

if "market_region" in df.columns:
    df["market_region"] = (
        df["market_region"]
        .str.strip()
        .str.title()
    )

if "sales_channel" in df.columns:
    df["sales_channel"] = (
        df["sales_channel"]
        .str.strip()
        .str.title()
    )


# --------------------------------------------------
# 6. Convert numerical columns
# --------------------------------------------------

numeric_columns = [
    "competitor_price",
    "feature_count",
    "market_rating",
    "estimated_market_share",
    "trend_score"
]

for column in numeric_columns:
    if column in df.columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )


# --------------------------------------------------
# 7. Validate competitor price
# --------------------------------------------------

if "competitor_price" in df.columns:

    df.loc[
        df["competitor_price"] <= 0,
        "competitor_price"
    ] = pd.NA


# --------------------------------------------------
# 8. Validate feature count
# --------------------------------------------------

if "feature_count" in df.columns:

    df.loc[
        df["feature_count"] < 0,
        "feature_count"
    ] = pd.NA


# --------------------------------------------------
# 9. Validate market rating
# --------------------------------------------------

if "market_rating" in df.columns:

    df.loc[
        ~df["market_rating"].between(0, 5),
        "market_rating"
    ] = pd.NA


# --------------------------------------------------
# 10. Validate market share
# --------------------------------------------------

if "estimated_market_share" in df.columns:

    df.loc[
        ~df["estimated_market_share"].between(0, 100),
        "estimated_market_share"
    ] = pd.NA


# --------------------------------------------------
# 11. Validate trend score
# --------------------------------------------------

if "trend_score" in df.columns:

    df.loc[
        ~df["trend_score"].between(0, 100),
        "trend_score"
    ] = pd.NA


# --------------------------------------------------
# 12. Remove rows missing critical information
# --------------------------------------------------

required_columns = [
    "competitor_id",
    "competitor_name",
    "category"
]

df = df.dropna(
    subset=required_columns
)


# --------------------------------------------------
# 13. Sort by category
# --------------------------------------------------

if "category" in df.columns:
    df = df.sort_values("category")


# --------------------------------------------------
# 14. Save cleaned dataset
# --------------------------------------------------

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# --------------------------------------------------
# 15. Display results
# --------------------------------------------------

print("\n" + "=" * 55)
print("COMPETITOR DATA CLEANING COMPLETE")
print("=" * 55)

print(f"Rows after cleaning: {len(df)}")
print(f"Rows removed: {before - len(df)}")

print(f"Output: {OUTPUT_FILE}")


print("\nMissing values:")
print(df.isnull().sum())


print("\nCompetitor categories:")
print(df["category"].value_counts())


print("\nMarket regions:")
print(df["market_region"].value_counts())


print("\nSample competitor records:")
print(df.head())