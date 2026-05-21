import logging
import time
from datetime import date, datetime, timezone
from typing import Optional

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from collector.github_client import GitHubClient, RateLimitError
from collector.languages import get_active_languages
from config.settings import settings
from core.metrics import get_stars_delta
from core.transformer import calculate_engagement_score
from db.models import CollectorRun, Repository, RepositorySnapshot
from db.session import SessionLocal

logger = logging.getLogger("meridian.collector")


def _upsert_repository(db: Session, repo_data: dict) -> int:
    stmt = (
        insert(Repository)
        .values(
            id=repo_data["id"],
            full_name=repo_data["full_name"],
            name=repo_data["name"],
            description=repo_data.get("description"),
            language=repo_data.get("language"),
            html_url=repo_data.get("html_url"),
            owner_login=repo_data["owner"]["login"],
            is_fork=repo_data.get("fork", False),
            created_at=repo_data.get("created_at"),
            updated_at=datetime.now(tz=timezone.utc),
        )
        .on_conflict_do_update(
            index_elements=["id"],
            set_={
                "description": repo_data.get("description"),
                "language": repo_data.get("language"),
                "updated_at": datetime.now(tz=timezone.utc),
            },
        )
    )
    db.execute(stmt)
    return repo_data["id"]


def _insert_snapshot(db: Session, repo_id: int, repo_data: dict) -> None:
    today = date.today()
    stars_delta_7d = get_stars_delta(db, repo_id, days=7)
    stars_delta_30d = get_stars_delta(db, repo_id, days=30)

    repo_created = repo_data.get("created_at")
    if repo_created:
        created_dt = datetime.fromisoformat(repo_created.replace("Z", "+00:00"))
        age_days = (datetime.now(tz=timezone.utc) - created_dt).days
    else:
        age_days = 365

    score = calculate_engagement_score(
        stars=repo_data.get("stargazers_count", 0),
        forks=repo_data.get("forks_count", 0),
        watchers=repo_data.get("watchers_count", 0),
        open_issues=repo_data.get("open_issues_count", 0),
        repo_age_days=age_days,
        stars_delta_30d=stars_delta_30d or 0,
    )

    stmt = (
        insert(RepositorySnapshot)
        .values(
            repository_id=repo_id,
            snapshot_date=today,
            stars_count=repo_data.get("stargazers_count", 0),
            forks_count=repo_data.get("forks_count", 0),
            watchers_count=repo_data.get("watchers_count", 0),
            open_issues_count=repo_data.get("open_issues_count", 0),
            network_count=repo_data.get("network_count"),
            subscribers_count=repo_data.get("subscribers_count"),
            engagement_score=score,
            stars_delta_7d=stars_delta_7d,
            stars_delta_30d=stars_delta_30d,
        )
        .on_conflict_do_update(
            constraint="uq_snapshot_per_day",
            set_={
                "stars_count": repo_data.get("stargazers_count", 0),
                "forks_count": repo_data.get("forks_count", 0),
                "watchers_count": repo_data.get("watchers_count", 0),
                "open_issues_count": repo_data.get("open_issues_count", 0),
                "engagement_score": score,
                "stars_delta_7d": stars_delta_7d,
                "stars_delta_30d": stars_delta_30d,
            },
        )
    )
    db.execute(stmt)


def collect_language(language: str, client: Optional[GitHubClient] = None) -> dict:
    if client is None:
        client = GitHubClient()

    db: Session = SessionLocal()
    run = CollectorRun(language=language, status="running")
    db.add(run)
    db.commit()

    collected = 0
    updated = 0
    start_time = time.time()

    try:
        logger.info("Starting collection for language: %s", language)
        result = client.search_repositories(language=language, per_page=settings.repos_per_language)
        repos = result.get("items", [])

        for repo_data in repos:
            try:
                full_data = client.get_repository(
                    repo_data["owner"]["login"], repo_data["name"]
                )
                repo_id = _upsert_repository(db, full_data)
                _insert_snapshot(db, repo_id, full_data)
                db.commit()
                collected += 1
            except RateLimitError:
                # Rate limit was hit and waited; retry once
                full_data = client.get_repository(
                    repo_data["owner"]["login"], repo_data["name"]
                )
                repo_id = _upsert_repository(db, full_data)
                _insert_snapshot(db, repo_id, full_data)
                db.commit()
                collected += 1
            except Exception as exc:
                db.rollback()
                logger.warning(
                    "Failed to collect repo %s: %s", repo_data.get("full_name"), exc
                )

        elapsed = round(time.time() - start_time, 2)
        run.status = "success"
        run.repos_collected = collected
        run.repos_updated = updated
        run.finished_at = datetime.now(tz=timezone.utc)
        db.commit()

        logger.info(
            "Collection finished for %s: %d repos in %.2fs",
            language, collected, elapsed,
        )
        return {"language": language, "collected": collected, "elapsed_seconds": elapsed}

    except Exception as exc:
        db.rollback()
        run.status = "error"
        run.error_message = str(exc)
        run.finished_at = datetime.now(tz=timezone.utc)
        db.commit()
        logger.error("Collection failed for %s: %s", language, exc)
        raise
    finally:
        db.close()


def run_full_collection() -> list[dict]:
    client = GitHubClient()
    languages = get_active_languages()
    results = []
    for lang in languages:
        try:
            result = collect_language(lang, client=client)
            results.append(result)
        except Exception as exc:
            results.append({"language": lang, "error": str(exc)})
    return results
