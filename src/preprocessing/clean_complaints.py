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
    / "complaints.csv"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
)

OUTPUT_FILE = OUTPUT_DIR / "complaints_clean.csv"


# -----------------------------------
# 2. Load dataset
# -----------------------------------

df = pd.read_csv(INPUT_FILE)

print("Raw complaints dataset loaded.")
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
# 4. Remove duplicate complaints
# -----------------------------------

before = len(df)

df = df.drop_duplicates(
    subset=["complaint_id"]
)

duplicates_removed = before - len(df)

print(
    f"Duplicate complaints removed: "
    f"{duplicates_removed}"
)


# -----------------------------------
# 5. Clean text columns
# -----------------------------------

text_columns = [
    "complaint_id",
    "company_id",
    "product_id",
    "customer_id",
    "complaint_category",
    "complaint_text",
    "priority",
    "status"
]

for column in text_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )


# -----------------------------------
# 6. Clean complaint text
# -----------------------------------

if "complaint_text" in df.columns:

    df["complaint_text"] = (
        df["complaint_text"]
        .str.replace(
            r"\s+",
            " ",
            regex=True
        )
    )

    df.loc[
        df["complaint_text"].str.len() == 0,
        "complaint_text"
    ] = pd.NA


# -----------------------------------
# 7. Standardize complaint category
# -----------------------------------

if "complaint_category" in df.columns:

    df["complaint_category"] = (
        df["complaint_category"]
        .str.strip()
        .str.lower()
    )


# -----------------------------------
# 8. Standardize priority
# -----------------------------------

if "priority" in df.columns:

    df["priority"] = (
        df["priority"]
        .str.strip()
        .str.title()
    )

    valid_priorities = [
        "Low",
        "Medium",
        "High",
        "Critical"
    ]

    df.loc[
        ~df["priority"].isin(valid_priorities),
        "priority"
    ] = pd.NA


# -----------------------------------
# 9. Standardize status
# -----------------------------------

if "status" in df.columns:

    df["status"] = (
        df["status"]
        .str.strip()
        .str.title()
    )

    valid_statuses = [
        "Open",
        "In Progress",
        "Resolved",
        "Closed"
    ]

    df.loc[
        ~df["status"].isin(valid_statuses),
        "status"
    ] = pd.NA


# -----------------------------------
# 10. Convert complaint date
# -----------------------------------

if "complaint_date" in df.columns:

    df["complaint_date"] = pd.to_datetime(
        df["complaint_date"],
        errors="coerce"
    )


# -----------------------------------
# 11. Remove invalid records
# -----------------------------------

required_columns = [
    "complaint_id",
    "company_id",
    "product_id",
    "customer_id",
    "complaint_text",
    "complaint_category"
]

df = df.dropna(
    subset=required_columns
)


# -----------------------------------
# 12. Sort by date
# -----------------------------------

if "complaint_date" in df.columns:

    df = df.sort_values(
        "complaint_date"
    )


# -----------------------------------
# 13. Create output directory
# -----------------------------------

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# -----------------------------------
# 14. Save
# -----------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# -----------------------------------
# 15. Verification
# -----------------------------------

print("\n" + "=" * 55)

print("COMPLAINT CLEANING COMPLETE")

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

print("\nComplaint categories:")

print(
    df["complaint_category"]
    .value_counts()
)

print("\nPriority distribution:")

print(
    df["priority"]
    .value_counts()
)

print("\nSample complaints:")

print(
    df[
        [
            "complaint_category",
            "complaint_text",
            "priority"
        ]
    ].head()
)