import pandas as pd
import os


INPUT_FILE = "data/features/evaluated_product_concepts.csv"
OUTPUT_FILE = "data/features/concept_risk_analysis.csv"


def calculate_risk(row):

    risk = 0

    solution = str(row["solution"]).lower()
    features = str(row["key_features"]).lower()

    # Technical complexity
    complex_terms = [
        "real-time",
        "autonomous",
        "robot",
        "iot",
        "computer vision",
        "predictive",
        "blockchain"
    ]

    risk += sum(
        5 for term in complex_terms
        if term in solution or term in features
    )

    # AI dependency
    if "ai" in solution or "machine learning" in solution:
        risk += 5

    # Hardware dependency
    hardware_terms = [
        "sensor",
        "device",
        "hardware",
        "wearable",
        "camera"
    ]

    risk += sum(
        4 for term in hardware_terms
        if term in solution or term in features
    )

    return min(risk, 100)


def risk_category(score):

    if score >= 60:
        return "High Risk"

    elif score >= 35:
        return "Moderate Risk"

    else:
        return "Low Risk"


def run_risk_analysis():

    print("CONCEPT RISK ANALYSIS ENGINE")
    print("-" * 60)

    df = pd.read_csv(INPUT_FILE)

    print(f"Concepts loaded: {len(df)}")

    df["risk_score"] = df.apply(
        calculate_risk,
        axis=1
    )

    df["risk_category"] = df["risk_score"].apply(
        risk_category
    )

    # Risk-adjusted score
    df["risk_adjusted_score"] = (
        df["overall_score"] - df["risk_score"] * 0.30
    ).round(2)

    # Final recommendation
    def final_recommendation(row):

        score = row["risk_adjusted_score"]

        if score >= 75:
            return "Proceed"

        elif score >= 60:
            return "Proceed with Validation"

        elif score >= 45:
            return "Needs Further Analysis"

        else:
            return "Do Not Prioritize"

    df["final_recommendation"] = df.apply(
        final_recommendation,
        axis=1
    )

    df = df.sort_values(
        by="risk_adjusted_score",
        ascending=False
    ).reset_index(drop=True)

    df["final_rank"] = range(
        1,
        len(df) + 1
    )

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nRISK ANALYSIS COMPLETE")
    print("-" * 60)

    print(f"Analyzed concepts: {len(df)}")
    print(f"Saved to: {OUTPUT_FILE}")

    print("\nFinal ranking:")
    print(
        df[
            [
                "product_name",
                "overall_score",
                "risk_score",
                "risk_adjusted_score",
                "final_recommendation"
            ]
        ].to_string(index=False)
    )


if __name__ == "__main__":
    run_risk_analysis()
    
    