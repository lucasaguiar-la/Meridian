from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel


class SnapshotOut(BaseModel):
    snapshot_date: date
    stars_count: int
    forks_count: int
    watchers_count: Optional[int]
    open_issues_count: Optional[int]
    engagement_score: Optional[float]
    stars_delta_7d: Optional[int]
    stars_delta_30d: Optional[int]

    model_config = {"from_attributes": True}


class RepositoryOut(BaseModel):
    id: int
    full_name: str
    name: str
    description: Optional[str]
    language: Optional[str]
    html_url: Optional[str]
    owner_login: Optional[str]
    is_fork: bool
    created_at: Optional[datetime]
    latest_snapshot: Optional[SnapshotOut] = None

    model_config = {"from_attributes": True}


class RepositoryListMeta(BaseModel):
    total: int
    language: Optional[str]
    limit: int
    offset: int


class RepositoryListOut(BaseModel):
    data: list[RepositoryOut]
    meta: RepositoryListMeta
