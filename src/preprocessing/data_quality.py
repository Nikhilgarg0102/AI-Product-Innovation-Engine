import pandas as pd
from pathlib import Path


# -----------------------------------
# 1. Project paths
# -----------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_ROOT = PROJECT_ROOT / "data" / "raw"


# -----------------------------------
# 2. Dataset locations
# -----------------------------------

DATASETS = {
    "companies": DATA_ROOT / "company" / "companies.csv",

    "products": DATA_ROOT / "company" / "products.csv",

    "customers": DATA_ROOT / "customers" / "customers.csv",

    "purchases": DATA_ROOT / "customers" / "purchases.csv",

    "reviews": DATA_ROOT / "customers" / "reviews.csv",

    "complaints": DATA_ROOT / "customers" / "complaints.csv",

    "surveys": DATA_ROOT / "customers" / "surveys.csv",

    "competitors": DATA_ROOT / "market" / "competitors.csv"
}


# -----------------------------------
# 3. Check one dataset
# -----------------------------------

def check_dataset(name, file_path):

    print("\n" + "=" * 60)

    print(f"DATASET: {name.upper()}")

    print("=" * 60)

    # Check file existence
    if not file_path.exists():

        print("❌ FILE NOT FOUND")

        return

    # Load dataset
    df = pd.read_csv(file_path)

    print(f"Rows: {len(df)}")

    print(f"Columns: {len(df.columns)}")

    print("\nColumns:")

    for column in df.columns:

        print(f"  - {column}")

    # Missing values
    missing = df.isnull().sum()

    missing_total = missing.sum()

    print("\nMissing values:")

    if missing_total == 0:

        print("  ✓ No missing values")

    else:

        for column, count in missing.items():

            if count > 0:

                print(
                    f"  ⚠ {column}: {count}"
                )

    # Duplicate rows
    duplicates = df.duplicated().sum()

    print("\nDuplicate rows:")

    if duplicates == 0:

        print("  ✓ No duplicate rows")

    else:

        print(
            f"  ⚠ {duplicates} duplicate rows"
        )

    # Data types
    print("\nData types:")

    print(df.dtypes.to_string())

    return df


# -----------------------------------
# 4. Run checks
# -----------------------------------

def main():

    print("\n")
    print("=" * 60)
    print("AI PRODUCT INNOVATION ENGINE")
    print("DATA QUALITY CHECK")
    print("=" * 60)

    datasets = {}

    for name, path in DATASETS.items():

        df = check_dataset(
            name,
            path
        )

        if df is not None:

            datasets[name] = df

    # -----------------------------------
    # Summary
    # -----------------------------------

    print("\n")
    print("=" * 60)
    print("DATA QUALITY SUMMARY")
    print("=" * 60)

    print(
        f"Datasets checked: "
        f"{len(datasets)}"
    )

    for name, df in datasets.items():

        missing = df.isnull().sum().sum()

        duplicates = df.duplicated().sum()

        if missing == 0 and duplicates == 0:

            status = "✓ PASS"

        else:

            status = "⚠ REVIEW"

        print(
            f"{name:<15} "
            f"{status}"
        )


if __name__ == "__main__":

    main()