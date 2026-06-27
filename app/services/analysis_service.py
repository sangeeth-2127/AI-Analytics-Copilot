from app.schemas.analysis import DatasetAnalysis
from app.schemas.profile import DatasetProfile
from app.schemas.statistics import DatasetStatistics
from app.schemas.insights import DatasetInsights

from app.analytics.profiling import profile_dataset
from app.analytics.statistics import generate_statistics
from app.analytics.insights import generate_insights


def analyze_dataset(df):

    profile = DatasetProfile(
        **profile_dataset(df)
    )

    statistics = DatasetStatistics(
        statistics=generate_statistics(df)
    )

    insights = DatasetInsights(
        **generate_insights(
            profile.model_dump(),
            statistics.statistics
        )
    )

    analysis = DatasetAnalysis(
        profile=profile,
        statistics=statistics,
        insights=insights,
    )

    return analysis