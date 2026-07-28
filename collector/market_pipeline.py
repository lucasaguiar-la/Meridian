import logging
from datetime import date
from typing import Optional

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from collector.languages import get_active_languages
from collector.market_client import AdzunaClient, RemoteOKClient
from db.models import JobMarketSnapshot
from db.session import SessionLocal

logger = logging.getLogger("meridian.market")

SOURCE_ADZUNA = "adzuna"
SOURCE_REMOTEOK = "remoteok"


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


def collect_adzuna_language(language: str, client: Optional[AdzunaClient] = None) -> dict:
    if client is None:
        client = AdzunaClient()

    db: Session = SessionLocal()
    today = date.today()

    try:
        count = client.count_job_postings(language)
        _upsert_snapshot(db, language, SOURCE_ADZUNA, today, count)
        db.commit()
        logger.info(
            "Collected Adzuna market snapshot for %s: %d open positions", language, count
        )
        return {"language": language, "source": SOURCE_ADZUNA, "open_positions_count": count}
    except Exception as exc:
        db.rollback()
        logger.warning("Failed to collect Adzuna market data for %s: %s", language, exc)
        return {"language": language, "source": SOURCE_ADZUNA, "error": str(exc)}
    finally:
        db.close()


def collect_remoteok_languages(
    languages: list[str], client: Optional[RemoteOKClient] = None
) -> list[dict]:
    """Fetches RemoteOK's listing batch once and records a snapshot per language from it."""
    if client is None:
        client = RemoteOKClient()

    try:
        listings = client.fetch_listings()
    except Exception as exc:
        logger.warning("Failed to fetch RemoteOK listings: %s", exc)
        return [
            {"language": lang, "source": SOURCE_REMOTEOK, "error": str(exc)}
            for lang in languages
        ]

    results = []
    for lang in languages:
        db: Session = SessionLocal()
        try:
            count = client.count_by_tag(listings, lang)
            _upsert_snapshot(db, lang, SOURCE_REMOTEOK, date.today(), count)
            db.commit()
            logger.info(
                "Collected RemoteOK market snapshot for %s: %d open positions", lang, count
            )
            results.append(
                {"language": lang, "source": SOURCE_REMOTEOK, "open_positions_count": count}
            )
        except Exception as exc:
            db.rollback()
            logger.warning("Failed to store RemoteOK market data for %s: %s", lang, exc)
            results.append({"language": lang, "source": SOURCE_REMOTEOK, "error": str(exc)})
        finally:
            db.close()

    return results


def run_full_market_collection() -> list[dict]:
    languages = get_active_languages()

    adzuna_client = AdzunaClient()
    results = [collect_adzuna_language(lang, client=adzuna_client) for lang in languages]
    results.extend(collect_remoteok_languages(languages))
    return results
