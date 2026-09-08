import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "customers" / "surveys.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "surveys_clean.csv"


# --------------------------------------------------
# 1. Load dataset
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("Raw surveys dataset loaded.")
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
# 3. Remove duplicate surveys
# --------------------------------------------------

before = len(df)

df = df.drop_duplicates(subset=["survey_id"])

duplicates_removed = before - len(df)

print(f"Duplicate surveys removed: {duplicates_removed}")


# --------------------------------------------------
# 4. Clean text columns
# --------------------------------------------------

text_columns = [
    "survey_id",
    "company_id",
    "customer_id",
    "preferred_feature",
    "purchase_factor",
    "improvement_area",
    "would_recommend"
]

for column in text_columns:
    if column in df.columns:
        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )


# --------------------------------------------------
# 5. Normalize survey text
# --------------------------------------------------

for column in [
    "preferred_feature",
    "purchase_factor",
    "improvement_area"
]:
    if column in df.columns:
        df[column] = df[column].str.replace(
            r"\s+",
            " ",
            regex=True
        )

        df.loc[
            df[column].str.len() == 0,
            column
        ] = pd.NA


# --------------------------------------------------
# 6. Clean satisfaction score
# --------------------------------------------------

if "satisfaction_score" in df.columns:

    df["satisfaction_score"] = pd.to_numeric(
        df["satisfaction_score"],
        errors="coerce"
    )

    # Keep satisfaction score between 1 and 5
    df.loc[
        ~df["satisfaction_score"].between(1, 5),
        "satisfaction_score"
    ] = pd.NA


# --------------------------------------------------
# 7. Clean recommendation field
# --------------------------------------------------

if "would_recommend" in df.columns:

    df["would_recommend"] = (
        df["would_recommend"]
        .str.strip()
        .str.title()
    )

    valid_values = [
        "Yes",
        "No"
    ]

    df.loc[
        ~df["would_recommend"].isin(valid_values),
        "would_recommend"
    ] = pd.NA


# --------------------------------------------------
# 8. Convert survey date
# --------------------------------------------------

if "survey_date" in df.columns:

    df["survey_date"] = pd.to_datetime(
        df["survey_date"],
        errors="coerce"
    )


# --------------------------------------------------
# 9. Remove rows missing critical information
# --------------------------------------------------

required_columns = [
    "survey_id",
    "company_id",
    "customer_id"
]

df = df.dropna(
    subset=required_columns
)


# --------------------------------------------------
# 10. Sort by date
# --------------------------------------------------

if "survey_date" in df.columns:
    df = df.sort_values("survey_date")


# --------------------------------------------------
# 11. Save cleaned dataset
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
# 12. Display results
# --------------------------------------------------

print("\n" + "=" * 55)
print("SURVEY CLEANING COMPLETE")
print("=" * 55)

print(f"Rows after cleaning: {len(df)}")
print(f"Rows removed: {before - len(df)}")

print(f"Output: {OUTPUT_FILE}")


print("\nMissing values:")
print(df.isnull().sum())


print("\nSatisfaction distribution:")
print(df["satisfaction_score"].value_counts().sort_index())


print("\nRecommendation distribution:")
print(df["would_recommend"].value_counts())


print("\nPreferred features:")
print(df["preferred_feature"].value_counts().head(10))


print("\nSample surveys:")
print(
    df[
        [
            "satisfaction_score",
            "preferred_feature",
            "purchase_factor",
            "improvement_area",
            "would_recommend"
        ]
    ].head()
)