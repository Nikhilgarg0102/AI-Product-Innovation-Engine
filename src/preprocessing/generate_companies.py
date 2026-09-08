import pandas as pd
from pathlib import Path


# -----------------------------------
# 1. Project paths
# -----------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_FILE = PROJECT_ROOT / "data" / "raw" / "company" / "companies.csv"


# -----------------------------------
# 2. Company data
# -----------------------------------

companies = [
    {
        "company_id": "C001",
        "company_name": "Titan",
        "industry": "Consumer Electronics",
        "country": "India",
        "target_market": "Global",
        "company_size": "Enterprise"
    },
    {
        "company_id": "C002",
        "company_name": "NovaTech",
        "industry": "Consumer Electronics",
        "country": "India",
        "target_market": "India",
        "company_size": "Large"
    },
    {
        "company_id": "C003",
        "company_name": "ApexWear",
        "industry": "Wearables",
        "country": "USA",
        "target_market": "Global",
        "company_size": "Enterprise"
    },
    {
        "company_id": "C004",
        "company_name": "GreenHome",
        "industry": "Home Appliances",
        "country": "Germany",
        "target_market": "Europe",
        "company_size": "Large"
    },
    {
        "company_id": "C005",
        "company_name": "UrbanGear",
        "industry": "Consumer Products",
        "country": "UK",
        "target_market": "Global",
        "company_size": "Medium"
    },
    {
        "company_id": "C006",
        "company_name": "TechSphere",
        "industry": "Consumer Electronics",
        "country": "Japan",
        "target_market": "Asia",
        "company_size": "Enterprise"
    },
    {
        "company_id": "C007",
        "company_name": "NextGen Labs",
        "industry": "Technology",
        "country": "India",
        "target_market": "Global",
        "company_size": "Medium"
    },
    {
        "company_id": "C008",
        "company_name": "PrimeLiving",
        "industry": "Home Products",
        "country": "Canada",
        "target_market": "North America",
        "company_size": "Large"
    },
    {
        "company_id": "C009",
        "company_name": "VisionWorks",
        "industry": "Consumer Electronics",
        "country": "South Korea",
        "target_market": "Global",
        "company_size": "Enterprise"
    },
    {
        "company_id": "C010",
        "company_name": "FutureEdge",
        "industry": "Technology",
        "country": "Singapore",
        "target_market": "Asia",
        "company_size": "Medium"
    }
]


# -----------------------------------
# 3. Convert to DataFrame
# -----------------------------------

df = pd.DataFrame(companies)


# -----------------------------------
# 4. Save CSV
# -----------------------------------

df.to_csv(OUTPUT_FILE, index=False)


print("Companies dataset created successfully!")
print(f"Location: {OUTPUT_FILE}")
print(f"Number of companies: {len(df)}")