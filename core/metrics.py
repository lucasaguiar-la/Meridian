from datetime import date, timedelta
from typing import Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from db.models import RepositorySnapshot


def get_stars_delta(
    db: Session,
    repository_id: int,
    days: int,
    current_stars: Optional[int] = None,
) -> Optional[int]:
    """Stars gained over the last `days` days.

    `current_stars` is the up-to-date star count (e.g. straight from the API).
    Pass it when today's snapshot has not been saved yet; otherwise the latest
    stored snapshot is used as the end of the window.
    """
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
    latest = current_stars
    if latest is None:
        latest = db.scalar(
            select(RepositorySnapshot.stars_count)
            .where(RepositorySnapshot.repository_id == repository_id)
            .order_by(RepositorySnapshot.snapshot_date.desc())
            .limit(1)
        )

    if oldest is None or latest is None:
        return None
    return latest - oldest
