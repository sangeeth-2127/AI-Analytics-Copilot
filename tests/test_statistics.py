import pandas as pd
import pytest

from app.analytics.statistics import generate_statistics


def test_generate_statistics_returns_descriptive_stats_for_numeric_columns():
    df = pd.DataFrame({
        "age": [20, 25, 30, 35],
        "score": [1.5, 2.5, 3.5, 4.5],
        "category": ["a", "b", "a", "b"],
    })

    stats = generate_statistics(df)

    assert set(stats.keys()) == {"age", "score"}
    assert stats["age"]["count"] == 4
    assert stats["age"]["mean"] == pytest.approx(27.5)
    assert stats["score"]["max"] == pytest.approx(4.5)


def test_generate_statistics_raises_for_empty_dataframe():
    df = pd.DataFrame(columns=["age"])

    with pytest.raises(ValueError):
        generate_statistics(df)
