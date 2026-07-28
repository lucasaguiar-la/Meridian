from datetime import date, datetime
from typing import Optional, Any, Literal
from pydantic import BaseModel


class ReportGenerateRequest(BaseModel):
    report_type: Literal["weekly", "monthly"]
    language: Optional[str] = None
    all_languages: bool = False


class ReportOut(BaseModel):
    id: int
    report_type: str
    language: Optional[str]
    period_start: date
    period_end: date
    content_json: Any
    generated_at: datetime

    model_config = {"from_attributes": True}


class TrendingOut(BaseModel):
    repository_id: int
    full_name: str
    language: Optional[str]
    description: Optional[str]
    html_url: Optional[str]
    stars_count: int
    stars_delta_7d: Optional[int]
    stars_delta_30d: Optional[int]
    engagement_score: Optional[float]
