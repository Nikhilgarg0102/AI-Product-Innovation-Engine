import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq


# ============================================================
# LLM PRODUCT CONCEPT GENERATOR
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_FILE = BASE_DIR / "data" / "features" / "innovation_opportunities.csv"
OUTPUT_FILE = BASE_DIR / "data" / "features" / "llm_product_concepts.csv"


# ------------------------------------------------------------
# Load environment variables
# ------------------------------------------------------------

load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")


# ------------------------------------------------------------
# Create Groq client
# ------------------------------------------------------------

client = Groq(api_key=api_key)


# ------------------------------------------------------------
# Generate one concept using the LLM
# ------------------------------------------------------------

def generate_concept(row):

    category = str(row.get("category", "Unknown"))
    complaint = str(row.get("complaint_category", "General"))
    problem_score = str(row.get("product_pain_score", "N/A"))
    demand_score = str(row.get("demand_problem_score", "N/A"))
    market_gap_score = str(row.get("market_gap_score", "N/A"))
    opportunity_score = str(row.get("opportunity_score", "N/A"))
    priority = str(row.get("priority", "Moderate"))

    prompt = f"""
You are an expert product innovation strategist.

Generate ONE realistic and commercially useful product concept
based on the following opportunity data.

CATEGORY:
{category}

CUSTOMER PAIN / COMPLAINT:
{complaint}

PRODUCT PAIN SCORE:
{problem_score}

DEMAND-PROBLEM SCORE:
{demand_score}

MARKET GAP SCORE:
{market_gap_score}

OVERALL OPPORTUNITY SCORE:
{opportunity_score}

PRIORITY:
{priority}

Return the answer using exactly these sections:

PRODUCT NAME:
TARGET CUSTOMER:
PROBLEM:
SOLUTION:
KEY FEATURES:
EXPECTED BENEFITS:
INNOVATION:
WHY NOW:

Keep the concept practical, specific, and differentiated.
Do not use generic phrases such as "smart solution" without explaining
what makes the product different.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior product innovation expert "
                    "specializing in AI-driven product discovery."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=700
    )

    return response.choices[0].message.content


# ------------------------------------------------------------
# Main pipeline
# ------------------------------------------------------------

def main():

    print("=" * 70)
    print("LLM PRODUCT CONCEPT GENERATION ENGINE")
    print("=" * 70)

    # Load opportunity data
    df = pd.read_csv(INPUT_FILE)

    print(f"Opportunities loaded: {len(df)}")

    # For the first test, generate only 5 concepts
    test_df = df.head(5).copy()

    results = []

    for index, row in test_df.iterrows():

        print(f"\nGenerating concept {index + 1}/{len(test_df)}...")

        try:

            concept = generate_concept(row)

            results.append({
                "opportunity_id": row.get("opportunity_id", index + 1),
                "category": row.get("category", ""),
                "opportunity_score": row.get("opportunity_score", ""),
                "priority": row.get("priority", ""),
                "llm_concept": concept
            })

            print("Concept generated successfully.")

        except Exception as e:

            print(f"Error generating concept: {e}")

    # Save results
    result_df = pd.DataFrame(results)

    result_df.to_csv(OUTPUT_FILE, index=False)

    print("\n" + "=" * 70)
    print("LLM GENERATION COMPLETE")
    print("=" * 70)

    print(f"Generated concepts: {len(result_df)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
    