import pandas as pd
from pathlib import Path


# ============================================================
# LLM CONCEPT PARSER
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "features" / "llm_product_concepts.csv"
OUTPUT_FILE = BASE_DIR / "data" / "features" / "structured_product_concepts.csv"


# ------------------------------------------------------------
# Parse one LLM response
# ------------------------------------------------------------

def parse_concept(text):

    fields = {
        "product_name": "",
        "target_customer": "",
        "problem": "",
        "solution": "",
        "key_features": "",
        "expected_benefits": "",
        "innovation": "",
        "why_now": ""
    }

    if pd.isna(text):
        return fields

    text = str(text)

    current_field = None

    field_mapping = {
        "PRODUCT NAME": "product_name",
        "TARGET CUSTOMER": "target_customer",
        "PROBLEM": "problem",
        "SOLUTION": "solution",
        "KEY FEATURES": "key_features",
        "EXPECTED BENEFITS": "expected_benefits",
        "INNOVATION": "innovation",
        "WHY NOW": "why_now"
    }

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        # Detect section heading
        matched = False

        for heading, column in field_mapping.items():

            clean_line = line.strip()

            # Remove markdown formatting such as **PRODUCT NAME:**
            clean_line = clean_line.replace("**", "").replace("__", "").strip()

            if clean_line.upper().startswith(heading + ":"):

                current_field = column

                value = clean_line.split(":", 1)[1].strip()

                if value:
                    fields[column] = value

                matched = True
                break

        if matched:
            continue

        # Add continuation lines to current section
        if current_field:
            if fields[current_field]:
                fields[current_field] += " " + line
            else:
                fields[current_field] = line

    return fields


# ------------------------------------------------------------
# Main
# ------------------------------------------------------------

def main():

    print("=" * 70)
    print("LLM CONCEPT STRUCTURING ENGINE")
    print("=" * 70)

    df = pd.read_csv(INPUT_FILE)

    print(f"Concepts loaded: {len(df)}")

    parsed_records = []

    for _, row in df.iterrows():

        parsed = parse_concept(row["llm_concept"])

        record = {
            "opportunity_id": row.get("opportunity_id", ""),
            "category": row.get("category", ""),
            "opportunity_score": row.get("opportunity_score", ""),
            "priority": row.get("priority", "")
        }

        record.update(parsed)

        parsed_records.append(record)

    structured_df = pd.DataFrame(parsed_records)

    structured_df.to_csv(OUTPUT_FILE, index=False)

    print("\nSTRUCTURED COLUMNS")
    print("-" * 70)

    print(structured_df.columns.tolist())

    print("\nOUTPUT")
    print(f"Saved to: {OUTPUT_FILE}")

    print("\n" + "=" * 70)
    print("CONCEPT STRUCTURING COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()