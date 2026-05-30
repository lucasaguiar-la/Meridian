import logging
from datetime import date, timedelta

from sqlalchemy import func, select, text
from sqlalchemy.dialects.postgresql import insert as pg_insert

from collector.languages import get_active_languages
from db.models import Report, Repository, RepositorySnapshot
from db.session import SessionLocal

logger = logging.getLogger("meridian.reports")

TOP_N = 10


def _top_repos(db, language, period_start, period_end, metric):
    latest_subq = (
        select(
            RepositorySnapshot.repository_id,
            RepositorySnapshot.stars_count,
            RepositorySnapshot.forks_count,
            RepositorySnapshot.engagement_score,
            RepositorySnapshot.stars_delta_7d,
            RepositorySnapshot.stars_delta_30d,
        )
        .where(RepositorySnapshot.snapshot_date >= period_start)
        .where(RepositorySnapshot.snapshot_date <= period_end)
        .order_by(
            RepositorySnapshot.repository_id,
            RepositorySnapshot.snapshot_date.desc(),
        )
        .distinct(RepositorySnapshot.repository_id)
        .subquery("latest")
    )

    stmt = (
        select(
            Repository.id,
            Repository.full_name,
            Repository.language,
            Repository.html_url,
            latest_subq.c.stars_count,
            latest_subq.c.forks_count,
            latest_subq.c.engagement_score,
            latest_subq.c.stars_delta_7d,
            latest_subq.c.stars_delta_30d,
        )
        .join(latest_subq, Repository.id == latest_subq.c.repository_id)
    )

    if language:
        stmt = stmt.where(
            text("lower(repositories.language) = lower(:lang)")
        ).params(lang=language)

    if metric == "stars":
        stmt = stmt.order_by(latest_subq.c.stars_count.desc().nullslast())
    elif metric == "engagement":
        stmt = stmt.order_by(latest_subq.c.engagement_score.desc().nullslast())
    elif metric == "growth_7d":
        stmt = stmt.order_by(latest_subq.c.stars_delta_7d.desc().nullslast())
    elif metric == "growth_30d":
        stmt = stmt.order_by(latest_subq.c.stars_delta_30d.desc().nullslast())

    rows = db.execute(stmt.limit(TOP_N)).all()
    return [
        {
            "rank": i + 1,
            "repository_id": r.id,
            "full_name": r.full_name,
            "language": r.language,
            "html_url": r.html_url,
            "stars_count": r.stars_count,
            "forks_count": r.forks_count,
            "engagement_score": round(r.engagement_score, 3) if r.engagement_score is not None else None,
            "stars_delta_7d": r.stars_delta_7d,
            "stars_delta_30d": r.stars_delta_30d,
        }
        for i, r in enumerate(rows)
    ]


def _upsert_report(db, report_type, language, period_start, period_end, content):
    stmt = (
        pg_insert(Report)
        .values(
            report_type=report_type,
            language=language,
            period_start=period_start,
            period_end=period_end,
            content_json=content,
        )
        .on_conflict_do_update(
            constraint="uq_report_per_period",
            set_={"content_json": content, "period_end": period_end},
        )
    )
    db.execute(stmt)
    db.commit()


def generate_report(report_type: str, language: str | None = None) -> bool:
    today = date.today()

    if report_type == "weekly":
        period_start = today - timedelta(days=7)
        growth_metric = "growth_7d"
    else:
        period_start = today - timedelta(days=30)
        growth_metric = "growth_30d"

    period_end = today

    db = SessionLocal()
    try:
        repos_count_stmt = select(func.count()).select_from(Repository)
        if language:
            repos_count_stmt = repos_count_stmt.where(
                text("lower(repositories.language) = lower(:lang)")
            ).params(lang=language)
        repos_tracked = db.scalar(repos_count_stmt) or 0

        content = {
            "language": language,
            "period_start": period_start.isoformat(),
            "period_end": period_end.isoformat(),
            "repos_tracked": repos_tracked,
            "top_by_stars": _top_repos(db, language, period_start, period_end, "stars"),
            "top_by_engagement": _top_repos(db, language, period_start, period_end, "engagement"),
            "top_by_growth": _top_repos(db, language, period_start, period_end, growth_metric),
        }

        _upsert_report(db, report_type, language, period_start, period_end, content)
        logger.info("Generated %s report for language=%s", report_type, language or "all")
        return True
    except Exception as exc:
        db.rollback()
        logger.error(
            "Failed to generate %s report for language=%s: %s",
            report_type, language, exc,
        )
        return False
    finally:
        db.close()


def run_weekly_reports():
    logger.info("Generating weekly reports...")
    for lang in get_active_languages():
        generate_report("weekly", lang)
    generate_report("weekly", None)
    logger.info("Weekly reports done.")


def run_monthly_reports():
    logger.info("Generating monthly reports...")
    for lang in get_active_languages():
        generate_report("monthly", lang)
    generate_report("monthly", None)
    logger.info("Monthly reports done.")
