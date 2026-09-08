import pandas as pd
from pathlib import Path


# ============================================================
# PRODUCT CONCEPT GENERATION ENGINE
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "features" / "innovation_opportunities.csv"
OUTPUT_FILE = BASE_DIR / "data" / "features" / "product_concepts.csv"


def generate_product_concepts():

    print("=" * 70)
    print("PRODUCT CONCEPT GENERATION ENGINE")
    print("=" * 70)

    # --------------------------------------------------------
    # 1. Load innovation opportunities
    # --------------------------------------------------------

    df = pd.read_csv(INPUT_FILE)

    print(f"Opportunities loaded: {len(df)}")

    # --------------------------------------------------------
    # 2. Generate product concepts
    # --------------------------------------------------------

    concepts = []

    for _, row in df.iterrows():

        category = str(row.get("category", "Unknown"))
        complaint = str(row.get("complaint_category", "General"))
        priority = str(row.get("priority", "Moderate"))
        opportunity_score = float(row.get("opportunity_score", 0))

        concept_name = f"{complaint.title()}-Focused {category} Innovation {len(concepts) + 1}"

        target_customer = (
            f"Customers looking for better {category.lower()} products"
        )

        problem = (
            f"Customers are experiencing {complaint.lower()} "
            f"related problems in existing {category.lower()} products."
        )

        solution = (
            f"Develop an improved {category.lower()} product "
            f"focused on solving {complaint.lower()} issues."
        )

        features = (
            f"Improved {complaint.lower()} management, "
            f"better reliability, enhanced user experience"
        )

        benefits = (
            "Higher customer satisfaction, reduced complaints, "
            "better product performance and stronger market positioning"
        )

        concepts.append({
            "concept_id": f"CONCEPT_{len(concepts) + 1:04d}",
            "category": category,
            "concept_name": concept_name,
            "target_customer": target_customer,
            "problem": problem,
            "proposed_solution": solution,
            "key_features": features,
            "expected_benefits": benefits,
            "opportunity_score": opportunity_score,
            "priority": priority
        })

    # --------------------------------------------------------
    # 3. Create dataframe
    # --------------------------------------------------------

    concepts_df = pd.DataFrame(concepts)

    # --------------------------------------------------------
    # 4. Save output
    # --------------------------------------------------------

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    concepts_df.to_csv(OUTPUT_FILE, index=False)

    # --------------------------------------------------------
    # 5. Display results
    # --------------------------------------------------------

    print("\nTOP PRODUCT CONCEPTS")
    print("-" * 70)

    print(
        concepts_df[
            [
                "concept_id",
                "category",
                "concept_name",
                "opportunity_score",
                "priority"
            ]
        ].head(10).to_string(index=False)
    )

    print("\nOUTPUT")
    print(f"Saved to: {OUTPUT_FILE}")

    return concepts_df


if __name__ == "__main__":
    generate_product_concepts()