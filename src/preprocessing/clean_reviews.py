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
    / "reviews.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

OUTPUT_FILE = OUTPUT_DIR / "reviews_clean.csv"


# -----------------------------------
# 2. Load dataset
# -----------------------------------

df = pd.read_csv(INPUT_FILE)

print("Raw reviews dataset loaded.")
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
# 4. Remove duplicate reviews
# -----------------------------------

before = len(df)

df = df.drop_duplicates(
    subset=["review_id"]
)

duplicates_removed = before - len(df)

print(
    f"Duplicate reviews removed: "
    f"{duplicates_removed}"
)


# -----------------------------------
# 5. Clean text fields
# -----------------------------------

text_columns = [
    "review_id",
    "company_id",
    "product_id",
    "customer_id",
    "review_text"
]

for column in text_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )


# -----------------------------------
# 6. Clean review text
# -----------------------------------

if "review_text" in df.columns:

    # Replace multiple spaces
    df["review_text"] = (
        df["review_text"]
        .str.replace(
            r"\s+",
            " ",
            regex=True
        )
    )

    # Remove empty reviews
    df.loc[
        df["review_text"].str.len() == 0,
        "review_text"
    ] = pd.NA


# -----------------------------------
# 7. Validate rating
# -----------------------------------

if "rating" in df.columns:

    df["rating"] = pd.to_numeric(
        df["rating"],
        errors="coerce"
    )

    # Ratings must be between 1 and 5
    df.loc[
        (df["rating"] < 1) |
        (df["rating"] > 5),
        "rating"
    ] = pd.NA


# -----------------------------------
# 8. Convert review date
# -----------------------------------

if "review_date" in df.columns:

    df["review_date"] = pd.to_datetime(
        df["review_date"],
        errors="coerce"
    )


# -----------------------------------
# 9. Clean verified purchase
# -----------------------------------

if "verified_purchase" in df.columns:

    df["verified_purchase"] = (
        df["verified_purchase"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({
            "true": True,
            "false": False
        })
    )


# -----------------------------------
# 10. Remove invalid records
# -----------------------------------

key_columns = [
    "review_id",
    "company_id",
    "product_id",
    "customer_id",
    "review_text"
]

df = df.dropna(
    subset=key_columns
)

df = df.dropna(
    subset=["rating"]
)


# -----------------------------------
# 11. Sort reviews
# -----------------------------------

if "review_date" in df.columns:

    df = df.sort_values(
        "review_date"
    )


# -----------------------------------
# 12. Create processed directory
# -----------------------------------

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# -----------------------------------
# 13. Save cleaned dataset
# -----------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# -----------------------------------
# 14. Final verification
# -----------------------------------

print("\n" + "=" * 55)

print("REVIEW CLEANING COMPLETE")

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

print("\nRating distribution:")

print(
    df["rating"]
    .value_counts()
    .sort_index()
)

print("\nSample reviews:")

print(
    df[
        [
            "review_text",
            "rating"
        ]
    ].head()
)