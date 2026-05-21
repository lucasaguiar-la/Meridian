from datetime import date, timedelta
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from db.models import RepositorySnapshot


def get_stars_delta(
    db: Session, repository_id: int, days: int
) -> Optional[int]:
    cutoff = date.today() - timedelta(days=days)

    oldest = db.scalar(
        select(RepositorySnapshot.stars_count)
        .where(
            RepositorySnapshot.repository_id == repository_id,
            RepositorySnapshot.snapshot_date >= cutoff,
        )
        .order_by(RepositorySnapshot.snapshot_date.asc())
        .limit(1)
    )
    latest = db.scalar(
        select(RepositorySnapshot.stars_count)
        .where(RepositorySnapshot.repository_id == repository_id)
        .order_by(RepositorySnapshot.snapshot_date.desc())
        .limit(1)
    )

    if oldest is None or latest is None:
        return None
    return latest - oldest
