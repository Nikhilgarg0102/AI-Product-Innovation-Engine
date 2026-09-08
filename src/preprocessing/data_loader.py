import pandas as pd
from pathlib import Path


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "processed"


# --------------------------------------------------
# Dataset loader
# --------------------------------------------------

def load_data():

    data = {}

    files = {
        "companies": "companies_clean.csv",
        "products": "products_clean.csv",
        "customers": "customers_clean.csv",
        "purchases": "purchases_clean.csv",
        "reviews": "reviews_clean.csv",
        "complaints": "complaints_clean.csv",
        "surveys": "surveys_clean.csv",
        "competitors": "competitors_clean.csv"
    }

    for name, filename in files.items():

        file_path = DATA_DIR / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {file_path}"
            )

        data[name] = pd.read_csv(file_path)

    return data


# --------------------------------------------------
# Test loader
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)
    print("AI PRODUCT INNOVATION ENGINE")
    print("UNIFIED DATA LOADER")
    print("=" * 60)

    data = load_data()

    print("\nDatasets loaded successfully:\n")

    for name, df in data.items():

        print(
            f"{name:<15} "
            f"{len(df):>8,} rows  |  "
            f"{len(df.columns):>2} columns"
        )

    print("\n" + "=" * 60)
    print("DATA LOADER TEST PASSED")
    print("=" * 60)