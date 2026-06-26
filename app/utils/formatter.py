"""
Formatter Module

Formats profiling, statistics, and insight results
into a clean, human-readable format.

Project: AI Analytics Copilot
Author: Sangeeth S
"""


def format_profile(profile: dict) -> str:
    """
    Format dataset profile information.

    Args:
        profile (dict): Dataset profile.

    Returns:
        str: Formatted profile.
    """

    output = []

    output.append("=" * 60)
    output.append("📊 DATASET PROFILE")
    output.append("=" * 60)

    output.append(f"Rows               : {profile['rows']:,}")
    output.append(f"Columns            : {profile['columns']}")
    output.append(
        f"Memory Usage       : {profile['memory_usage_bytes'] / (1024 * 1024):.2f} MB"
    )
    output.append(f"Duplicate Rows     : {profile['duplicate_rows']}")

    output.append("\nColumn Names")
    output.append("-" * 60)

    for column in profile["column_names"]:
        output.append(f"• {column}")

    output.append("\nData Types")
    output.append("-" * 60)

    for column, dtype in profile["data_types"].items():
        output.append(f"{column:<35} {dtype}")

    output.append("\nMissing Values")
    output.append("-" * 60)

    for column, count in profile["missing_values"].items():
        output.append(f"{column:<35} {count}")

    return "\n".join(output)


def format_statistics(statistics: dict) -> str:
    """
    Format descriptive statistics.

    Args:
        statistics (dict): Statistics dictionary.

    Returns:
        str: Formatted statistics.
    """

    output = []

    output.append("=" * 60)
    output.append("📈 DATASET STATISTICS")
    output.append("=" * 60)

    for column, values in statistics.items():

        output.append(f"\n📌 {column}")
        output.append("-" * 60)

        output.append(f"Count              : {values['count']}")
        output.append(f"Mean               : {values['mean']:.2f}")
        output.append(f"Median             : {values['median']:.2f}")
        output.append(f"Minimum            : {values['min']:.2f}")
        output.append(f"Maximum            : {values['max']:.2f}")
        output.append(f"Standard Deviation : {values['std']:.2f}")

        # Optional (if present in statistics.py)
        if "variance" in values:
            output.append(f"Variance           : {values['variance']:.2f}")

        if "unique_values" in values:
            output.append(f"Unique Values      : {values['unique_values']}")

        if "missing_values" in values:
            output.append(f"Missing Values     : {values['missing_values']}")

    return "\n".join(output)


def format_insights(insight_report: dict) -> str:
    """
    Format AI-generated insights.

    Args:
        insight_report (dict): Dictionary containing summary and insights.

    Returns:
        str: Formatted insight report.
    """

    output = []

    output.append("=" * 60)
    output.append("🧠 AI ANALYTICS INSIGHTS")
    output.append("=" * 60)

    output.append("\n📋 SUMMARY")
    output.append("-" * 60)
    output.append(insight_report["summary"])

    output.append("\n💡 INSIGHTS")
    output.append("-" * 60)

    for insight in insight_report["insights"]:

        output.append(f"[{insight['type']}]")
        output.append(f"• {insight['message']}")
        output.append("")

    return "\n".join(output)