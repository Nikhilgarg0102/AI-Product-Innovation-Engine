import pandas as pd
import os


DATA_DIR = "data/processed"
OUTPUT_FILE = "data/knowledge_base/company_knowledge.txt"


def build_knowledge_base():

    print("KNOWLEDGE BASE BUILDER")
    print("-" * 60)

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    files = {
        "Companies": "companies_clean.csv",
        "Products": "products_clean.csv",
        "Customers": "customers_clean.csv",
        "Purchases": "purchases_clean.csv",
        "Reviews": "reviews_clean.csv",
        "Complaints": "complaints_clean.csv",
        "Surveys": "surveys_clean.csv",
        "Competitors": "competitors_clean.csv"
    }

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as knowledge_file:

        for section, filename in files.items():

            path = os.path.join(
                DATA_DIR,
                filename
            )

            print(f"Processing: {filename}")

            df = pd.read_csv(path)

            knowledge_file.write(
                f"\n\n{'=' * 70}\n"
            )

            knowledge_file.write(
                f"{section.upper()}\n"
            )

            knowledge_file.write(
                f"{'=' * 70}\n\n"
            )

            # Write records in a readable format
            for _, row in df.iterrows():

                record = []

                for column in df.columns:

                    value = row[column]

                    if pd.notna(value):

                        record.append(
                            f"{column}: {value}"
                        )

                knowledge_file.write(
                    " | ".join(record) + "\n"
                )

    print("\nKNOWLEDGE BASE CREATED")
    print("-" * 60)

    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    build_knowledge_base()