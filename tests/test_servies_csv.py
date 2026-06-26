from pathlib import Path

from app.analytics.insights import generate_insights
from app.analytics.profiling import profile_dataset
from app.analytics.statistics import generate_statistics
from app.services.csv_service import load_csv
from app.utils.formatter import (
    format_insights,
    format_profile,
    format_statistics,
)


def main():

    csv_path = Path("data/raw/Fifa.csv")

    df = load_csv(csv_path)

    profile = profile_dataset(df)

    statistics = generate_statistics(df)

    insights = generate_insights(profile, statistics)

    print(format_profile(profile))
    print()

    print(format_statistics(statistics))
    print()

    print(format_insights(insights))


if __name__ == "__main__":
    main()