from datetime import date
from typing import Optional
from pydantic import BaseModel


class MarketSnapshotOut(BaseModel):
    source: str
    snapshot_date: date
    open_positions_count: int
    avg_salary: Optional[float] = None

    model_config = {"from_attributes": True}


class LanguageMarketOut(BaseModel):
    language: str
    data: list[MarketSnapshotOut]
