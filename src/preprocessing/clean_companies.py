import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "company"
    / "companies.csv"
)

OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_FILE = (
    OUTPUT_DIR
    / "companies_clean.csv"
)


# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("Raw companies dataset loaded.")
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
# 3. Remove duplicate companies
# --------------------------------------------------

before = len(df)

df = df.drop_duplicates(
    subset=["company_id"]
)

duplicates_removed = before - len(df)

print(
    f"Duplicate companies removed: "
    f"{duplicates_removed}"
)


# --------------------------------------------------
# 4. Clean text columns
# --------------------------------------------------

text_columns = [
    "company_id",
    "company_name",
    "industry",
    "country",
    "target_market",
    "company_size"
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

if "company_name" in df.columns:

    df["company_name"] = (
        df["company_name"]
        .str.replace(
            r"\s+",
            " ",
            regex=True
        )
    )


if "industry" in df.columns:

    df["industry"] = (
        df["industry"]
        .str.strip()
        .str.title()
    )


if "country" in df.columns:

    df["country"] = (
        df["country"]
        .str.strip()
        .str.title()
    )


if "target_market" in df.columns:

    df["target_market"] = (
        df["target_market"]
        .str.strip()
        .str.title()
    )


if "company_size" in df.columns:

    df["company_size"] = (
        df["company_size"]
        .str.strip()
        .str.title()
    )


# --------------------------------------------------
# 6. Remove companies without IDs/names
# --------------------------------------------------

required_columns = [
    "company_id",
    "company_name"
]

df = df.dropna(
    subset=required_columns
)


# --------------------------------------------------
# 7. Sort companies
# --------------------------------------------------

df = df.sort_values(
    "company_id"
)


# --------------------------------------------------
# 8. Save cleaned dataset
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
# 9. Display results
# --------------------------------------------------

print("\n" + "=" * 55)
print("COMPANY CLEANING COMPLETE")
print("=" * 55)

print(
    f"Rows after cleaning: "
    f"{len(df)}"
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


print("\nCompanies:")
print(
    df[
        [
            "company_id",
            "company_name",
            "industry",
            "country",
            "target_market",
            "company_size"
        ]
    ]
)


print("\nCompany count:")
print(
    df["company_name"].nunique()
)