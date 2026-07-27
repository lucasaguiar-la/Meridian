import logging
from datetime import date
from typing import Optional

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from collector.languages import get_active_languages
from collector.market_client import AdzunaClient
from db.models import JobMarketSnapshot
from db.session import SessionLocal

logger = logging.getLogger("meridian.market")

SOURCE_ADZUNA = "adzuna"


def _upsert_snapshot(
    db: Session, language: str, source: str, snapshot_date: date, open_positions_count: int
) -> None:
    stmt = (
        insert(JobMarketSnapshot)
        .values(
            language=language,
            source=source,
            snapshot_date=snapshot_date,
            open_positions_count=open_positions_count,
        )
        .on_conflict_do_update(
            constraint="uq_market_snapshot_per_day",
            set_={"open_positions_count": open_positions_count},
        )
    )
    db.execute(stmt)


def collect_market_language(language: str, client: Optional[AdzunaClient] = None) -> dict:
    if client is None:
        client = AdzunaClient()

    db: Session = SessionLocal()
    today = date.today()

    try:
        count = client.count_job_postings(language)
        _upsert_snapshot(db, language, SOURCE_ADZUNA, today, count)
        db.commit()
        logger.info(
            "Collected market snapshot for %s: %d open positions", language, count
        )
        return {"language": language, "source": SOURCE_ADZUNA, "open_positions_count": count}
    except Exception as exc:
        db.rollback()
        logger.warning("Failed to collect market data for %s: %s", language, exc)
        return {"language": language, "source": SOURCE_ADZUNA, "error": str(exc)}
    finally:
        db.close()


def run_full_market_collection() -> list[dict]:
    client = AdzunaClient()
    results = []
    for lang in get_active_languages():
        results.append(collect_market_language(lang, client=client))
    return results
