"""
Insight Generation Module

Converts dataset profile and statistics into
human-readable insights.

Project: AI Analytics Copilot
Author: Sangeeth S
"""


def generate_insights(profile: dict, statistics: dict) -> dict:
    

    insights = []

    # ------------------------------
    # Dataset Summary
    # ------------------------------

    summary = (
        f"The dataset contains "
        f"{profile['rows']:,} rows "
        f"and {profile['columns']} columns."
    )

    # ------------------------------
    # Dataset Size
    # ------------------------------

    if profile["rows"] > 100000:
        insights.append({
            "type": "Dataset",
            "message":
            "This is a large dataset suitable for machine learning."
        })
    else:
        insights.append({
            "type": "Dataset",
            "message":
            "This is a small to medium-sized dataset suitable for exploratory data analysis."
        })

    # ------------------------------
    # Duplicate Analysis
    # ------------------------------

    duplicates = profile["duplicate_rows"]

    if duplicates == 0:
        insights.append({
            "type": "Data Quality",
            "message":
            "No duplicate rows were detected."
        })
    else:
        insights.append({
            "type": "Data Quality",
            "message":
            f"{duplicates} duplicate rows were detected."
        })

    # ------------------------------
    # Missing Values
    # ------------------------------

    missing_found = False

    for column, count in profile["missing_values"].items():

        if count > 0:

            missing_found = True

            insights.append({
                "type": "Missing Values",
                "message":
                f"Column '{column}' contains {count} missing values."
            })

    if not missing_found:

        insights.append({
            "type": "Data Quality",
            "message":
            "No missing values were detected."
        })

    # ------------------------------
    # Statistics
    # ------------------------------

    for column, values in statistics.items():

        insights.append({

            "type": "Statistics",

            "message":
            f"The average value of '{column}' "
            f"is {values['mean']:.2f}."

        })

    return {

        "summary": summary,

        "insights": insights

    }