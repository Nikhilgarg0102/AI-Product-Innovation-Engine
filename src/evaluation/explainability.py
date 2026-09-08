import pandas as pd
import os


INPUT_FILE = "data/features/concept_risk_analysis.csv"
OUTPUT_FILE = "data/features/concept_explanations.csv"


def generate_explanation(row):

    reasons = []

    # Market opportunity
    if row["market_fit_score"] >= 70:
        reasons.append("Strong market opportunity")
    elif row["market_fit_score"] >= 50:
        reasons.append("Moderate market opportunity")
    else:
        reasons.append("Weak market opportunity")

    # Problem
    if row["problem_severity_score"] >= 70:
        reasons.append("Addresses a significant customer problem")
    elif row["problem_severity_score"] >= 50:
        reasons.append("Addresses a moderate customer problem")
    else:
        reasons.append("Customer problem severity is relatively low")

    # Innovation
    if row["innovation_score"] >= 70:
        reasons.append("Strong innovation potential")
    else:
        reasons.append("Innovation potential requires validation")

    # Feasibility
    if row["feasibility_score"] >= 80:
        reasons.append("Technically feasible")
    elif row["feasibility_score"] >= 60:
        reasons.append("Feasibility appears reasonable")
    else:
        reasons.append("Technical feasibility requires investigation")

    # Risk
    if row["risk_score"] < 35:
        reasons.append("Low implementation risk")
    elif row["risk_score"] < 60:
        reasons.append("Moderate implementation risk")
    else:
        reasons.append("High implementation risk")

    return "; ".join(reasons)


def run_explainability():

    print("CONCEPT EXPLAINABILITY ENGINE")
    print("-" * 60)

    df = pd.read_csv(INPUT_FILE)

    print(f"Concepts loaded: {len(df)}")

    df["decision_explanation"] = df.apply(
        generate_explanation,
        axis=1
    )

    # Main decision factors
    df["primary_strength"] = df[
        [
            "market_fit_score",
            "problem_severity_score",
            "innovation_score",
            "feasibility_score"
        ]
    ].idxmax(axis=1)

    df["primary_weakness"] = df[
        [
            "market_fit_score",
            "problem_severity_score",
            "innovation_score",
            "feasibility_score"
        ]
    ].idxmin(axis=1)

    os.makedirs(
        os.path.dirname(OUTPUT_FILE),
        exist_ok=True
    )

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nEXPLAINABILITY COMPLETE")
    print("-" * 60)

    print(f"Concepts explained: {len(df)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    run_explainability()