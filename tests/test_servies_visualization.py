from pathlib import Path

from app.services.csv_service import load_csv
from app.visualization.visualization_engine import generate_visualizations


def main():
    csv_path = Path("data/raw/fifa.csv")

    df = load_csv(csv_path)

    visualizations = generate_visualizations(df)

    print(visualizations.keys())


if __name__ == "__main__":
    main()