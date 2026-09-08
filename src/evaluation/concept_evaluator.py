import pandas as pd
import os


INPUT_FILE = "data/features/structured_product_concepts.csv"
OUTPUT_FILE = "data/features/evaluated_product_concepts.csv"


def evaluate_concepts():

    print("CONCEPT EVALUATION ENGINE")
    print("-" * 60)

    df = pd.read_csv(INPUT_FILE)

    print(f"Concepts loaded: {len(df)}")

    # --------------------------------------------------
    # Base scores
    # --------------------------------------------------

    # Market fit is derived from the original opportunity score
    df["market_fit_score"] = df["opportunity_score"].clip(0, 100)

    # Problem severity
    df["problem_severity_score"] = (
        df["opportunity_score"] * 0.8
    ).clip(0, 100)

    # Innovation score
    innovation_keywords = [
        "AI",
        "smart",
        "intelligent",
        "predictive",
        "adaptive",
        "automated",
        "personalized",
        "real-time"
    ]

    def calculate_innovation(text):
        text = str(text).lower()

        matches = sum(
            1 for keyword in innovation_keywords
            if keyword.lower() in text
        )

        return min(50 + matches * 7, 100)

    df["innovation_score"] = (
        df["innovation"].apply(calculate_innovation)
    )

    # --------------------------------------------------
    # Feasibility
    # --------------------------------------------------

    def calculate_feasibility(text):

        text = str(text).lower()

        difficult_terms = [
            "quantum",
            "teleportation",
            "fusion reactor",
            "mind reading",
            "impossible"
        ]

        difficulty = sum(
            1 for term in difficult_terms
            if term in text
        )

        return max(100 - difficulty * 20, 60)

    df["feasibility_score"] = (
        df["solution"].apply(calculate_feasibility)
    )

    # --------------------------------------------------
    # Overall score
    # --------------------------------------------------

    df["overall_score"] = (
        df["market_fit_score"] * 0.30
        + df["problem_severity_score"] * 0.25
        + df["innovation_score"] * 0.20
        + df["feasibility_score"] * 0.25
    ).round(2)

    # --------------------------------------------------
    # Recommendation
    # --------------------------------------------------

    def recommendation(score):

        if score >= 80:
            return "Highly Recommended"

        elif score >= 65:
            return "Recommended"

        elif score >= 50:
            return "Needs Review"

        else:
            return "Low Potential"

    df["recommendation"] = (
        df["overall_score"].apply(recommendation)
    )

    # --------------------------------------------------
    # Ranking
    # --------------------------------------------------

    df = df.sort_values(
        by="overall_score",
        ascending=False
    ).reset_index(drop=True)

    df["evaluation_rank"] = range(1, len(df) + 1)

    # --------------------------------------------------
    # Save
    # --------------------------------------------------

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nEVALUATION COMPLETE")
    print("-" * 60)

    print(f"Evaluated concepts: {len(df)}")
    print(f"Saved to: {OUTPUT_FILE}")

    print("\nTop concepts:")
    print(
        df[
            [
                "product_name",
                "overall_score",
                "recommendation"
            ]
        ].head(5).to_string(index=False)
    )


if __name__ == "__main__":
    evaluate_concepts()