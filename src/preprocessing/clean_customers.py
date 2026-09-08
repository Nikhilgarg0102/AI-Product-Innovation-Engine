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
    / "customers.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

OUTPUT_FILE = OUTPUT_DIR / "customers_clean.csv"


# -----------------------------------
# 2. Load dataset
# -----------------------------------

df = pd.read_csv(INPUT_FILE)

print("Raw customers dataset loaded.")
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
# 4. Remove duplicate customers
# -----------------------------------

before = len(df)

df = df.drop_duplicates(
    subset=["customer_id"]
)

duplicates_removed = before - len(df)

print(
    f"Duplicate customers removed: "
    f"{duplicates_removed}"
)


# -----------------------------------
# 5. Clean text columns
# -----------------------------------

text_columns = [
    "customer_id",
    "company_id",
    "gender",
    "city",
    "occupation"
]

for column in text_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
        )


# -----------------------------------
# 6. Clean age
# -----------------------------------

if "age" in df.columns:

    df["age"] = pd.to_numeric(
        df["age"],
        errors="coerce"
    )

    # Keep realistic age range
    df.loc[
        (df["age"] < 13) |
        (df["age"] > 100),
        "age"
    ] = pd.NA


# -----------------------------------
# 7. Clean income
# -----------------------------------

if "income" in df.columns:

    df["income"] = pd.to_numeric(
        df["income"],
        errors="coerce"
    )

    # Income cannot be negative
    df.loc[
        df["income"] < 0,
        "income"
    ] = pd.NA


# -----------------------------------
# 8. Standardize gender
# -----------------------------------

if "gender" in df.columns:

    df["gender"] = (
        df["gender"]
        .str.strip()
        .str.lower()
    )

    gender_mapping = {
        "m": "Male",
        "male": "Male",
        "f": "Female",
        "female": "Female",
        "other": "Other"
    }

    df["gender"] = (
        df["gender"]
        .map(gender_mapping)
        .fillna("Unknown")
    )


# -----------------------------------
# 9. Remove rows without IDs
# -----------------------------------

df = df.dropna(
    subset=["customer_id"]
)


# -----------------------------------
# 10. Sort
# -----------------------------------

df = df.sort_values(
    "customer_id"
)


# -----------------------------------
# 11. Create processed directory
# -----------------------------------

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# -----------------------------------
# 12. Save cleaned dataset
# -----------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# -----------------------------------
# 13. Final report
# -----------------------------------

print("\n" + "=" * 50)

print("CUSTOMER CLEANING COMPLETE")

print("=" * 50)

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

print("\nGender distribution:")

if "gender" in df.columns:
    print(df["gender"].value_counts())

print("\nFirst 5 customers:")

print(df.head())
