"""
Analysis Schemas

Pydantic models for complete dataset analysis.

Project: AI Analytics Copilot
Author: Sangeeth S
"""

from pydantic import BaseModel, Field

from app.schemas.profile import DatasetProfile
from app.schemas.statistics import DatasetStatistics
from app.schemas.insights import DatasetInsights