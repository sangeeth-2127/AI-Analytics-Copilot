from pathlib import Path
from app.analytics.profiling import profile_dataset
from app.services.csv_service import load_csv
from app.utils.formatter import format_profile


def main():
    csv_path = Path("data/raw/Fifa.csv")

    df = load_csv(csv_path)

    profile = profile_dataset(df)

    formatted_output = format_profile(profile)

    print(formatted_output)

if __name__ == "__main__":
    main()