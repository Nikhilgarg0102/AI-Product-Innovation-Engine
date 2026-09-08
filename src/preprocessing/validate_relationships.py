import pandas as pd
from pathlib import Path


# --------------------------------------------------
# Project paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data" / "processed"


# --------------------------------------------------
# Load datasets
# --------------------------------------------------

companies = pd.read_csv(
    DATA_DIR / "companies_clean.csv"
) if (DATA_DIR / "companies_clean.csv").exists() else None

products = pd.read_csv(
    DATA_DIR / "products_clean.csv"
)

customers = pd.read_csv(
    DATA_DIR / "customers_clean.csv"
)

purchases = pd.read_csv(
    DATA_DIR / "purchases_clean.csv"
)

reviews = pd.read_csv(
    DATA_DIR / "reviews_clean.csv"
)

complaints = pd.read_csv(
    DATA_DIR / "complaints_clean.csv"
)

surveys = pd.read_csv(
    DATA_DIR / "surveys_clean.csv"
)

competitors = pd.read_csv(
    DATA_DIR / "competitors_clean.csv"
)


print("=" * 65)
print("DATA RELATIONSHIP VALIDATION")
print("=" * 65)


# --------------------------------------------------
# Helper function
# --------------------------------------------------

def check_relationship(
    child_df,
    child_column,
    parent_df,
    parent_column,
    relationship_name
):

    child_ids = set(
        child_df[child_column]
        .dropna()
        .astype(str)
    )

    parent_ids = set(
        parent_df[parent_column]
        .dropna()
        .astype(str)
    )

    invalid_ids = child_ids - parent_ids

    print(f"\n{relationship_name}")

    print(f"Child unique IDs : {len(child_ids)}")
    print(f"Parent unique IDs: {len(parent_ids)}")
    print(f"Invalid IDs      : {len(invalid_ids)}")

    if invalid_ids:
        print("Status: ❌ FAILED")
        print("Examples:", list(invalid_ids)[:5])
    else:
        print("Status: ✅ PASSED")


# --------------------------------------------------
# Product relationships
# --------------------------------------------------

check_relationship(
    purchases,
    "product_id",
    products,
    "product_id",
    "Purchases → Products"
)

check_relationship(
    reviews,
    "product_id",
    products,
    "product_id",
    "Reviews → Products"
)

check_relationship(
    complaints,
    "product_id",
    products,
    "product_id",
    "Complaints → Products"
)


# --------------------------------------------------
# Customer relationships
# --------------------------------------------------

check_relationship(
    purchases,
    "customer_id",
    customers,
    "customer_id",
    "Purchases → Customers"
)

check_relationship(
    reviews,
    "customer_id",
    customers,
    "customer_id",
    "Reviews → Customers"
)

check_relationship(
    complaints,
    "customer_id",
    customers,
    "customer_id",
    "Complaints → Customers"
)

check_relationship(
    surveys,
    "customer_id",
    customers,
    "customer_id",
    "Surveys → Customers"
)


# --------------------------------------------------
# Company relationships
# --------------------------------------------------

check_relationship(
    products,
    "company_id",
    customers,
    "company_id",
    "Products → Companies represented in Customers"
)

check_relationship(
    purchases,
    "company_id",
    customers,
    "company_id",
    "Purchases → Companies"
)


# --------------------------------------------------
# Cross-check company consistency
# --------------------------------------------------

print("\n" + "=" * 65)
print("COMPANY CONSISTENCY CHECK")
print("=" * 65)


product_company = (
    products[
        ["product_id", "company_id"]
    ]
    .drop_duplicates("product_id")
    .set_index("product_id")["company_id"]
)


purchase_company_check = purchases.copy()

purchase_company_check["product_company_id"] = (
    purchase_company_check["product_id"]
    .map(product_company)
)


inconsistent_purchases = (
    purchase_company_check[
        purchase_company_check["company_id"]
        != purchase_company_check["product_company_id"]
    ]
)


print(
    f"Purchases with company mismatch: "
    f"{len(inconsistent_purchases)}"
)


if len(inconsistent_purchases) == 0:
    print("Status: ✅ PASSED")
else:
    print("Status: ❌ FAILED")


# --------------------------------------------------
# Final summary
# --------------------------------------------------

print("\n" + "=" * 65)
print("RELATIONSHIP VALIDATION COMPLETE")
print("=" * 65)

print("\nDataset sizes:")

print(f"Products     : {len(products):,}")
print(f"Customers    : {len(customers):,}")
print(f"Purchases    : {len(purchases):,}")
print(f"Reviews      : {len(reviews):,}")
print(f"Complaints   : {len(complaints):,}")
print(f"Surveys      : {len(surveys):,}")
print(f"Competitors  : {len(competitors):,}")