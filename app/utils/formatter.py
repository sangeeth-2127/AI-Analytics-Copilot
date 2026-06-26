"""
Formatter Module

Formats dataset profile information into a readable format.

Project: AI Analytics Copilot
Author: Sangeeth S
"""


def format_profile(profile: dict) -> str:
    """
    Format the dataset profile into a readable string.

    Args:
        profile (dict): Dataset profile dictionary.

    Returns:
        str: Formatted dataset profile.
    """

    output = []

    output.append("=" * 50)
    output.append("📊 DATASET PROFILE")
    output.append("=" * 50)

    output.append(f"Rows              : {profile['rows']:,}")
    output.append(f"Columns           : {profile['columns']}")
    output.append(
        f"Memory Usage      : {profile['memory_usage_bytes'] / (1024 * 1024):.2f} MB"
    )
    output.append(f"Duplicate Rows    : {profile['duplicate_rows']}")

    output.append("\nColumn Names")
    output.append("-" * 50)

    for column in profile["column_names"]:
        output.append(f"• {column}")

    output.append("\nData Types")
    output.append("-" * 50)

    for column, dtype in profile["data_types"].items():
        output.append(f"{column:<30} {dtype}")

    output.append("\nMissing Values")
    output.append("-" * 50)

    for column, count in profile["missing_values"].items():
        output.append(f"{column:<30} {count}")

    return "\n".join(output)