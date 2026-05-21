from datetime import date, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from api.dependencies import get_db
from api.schemas.report import ReportOut, TrendingOut
from db.models import Report, RepositorySnapshot, Repository

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/trending")
def get_trending(
    language: Optional[str] = None,
    days: int = Query(7, ge=1, le=30),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    cutoff = date.today() - timedelta(days=days)

    latest_subq = (
        select(
            RepositorySnapshot.repository_id,
            RepositorySnapshot.stars_count,
            RepositorySnapshot.stars_delta_7d,
            RepositorySnapshot.stars_delta_30d,
            RepositorySnapshot.engagement_score,
        )
        .where(RepositorySnapshot.snapshot_date >= cutoff)
        .order_by(
            RepositorySnapshot.repository_id,
            RepositorySnapshot.snapshot_date.desc(),
        )
        .distinct(RepositorySnapshot.repository_id)
        .subquery("latest")
    )

    stmt = (
        select(
            Repository.id.label("repository_id"),
            Repository.full_name,
            Repository.language,
            Repository.description,
            Repository.html_url,
            latest_subq.c.stars_count,
            latest_subq.c.stars_delta_7d,
            latest_subq.c.stars_delta_30d,
            latest_subq.c.engagement_score,
        )
        .join(latest_subq, Repository.id == latest_subq.c.repository_id)
    )

    if language:
        stmt = stmt.where(text("lower(repositories.language) = lower(:lang)")).params(lang=language)

    order_col = latest_subq.c.stars_delta_7d if days <= 7 else latest_subq.c.stars_delta_30d
    stmt = stmt.order_by(order_col.desc().nullslast()).limit(limit)

    rows = db.execute(stmt).all()
    return {
        "data": [
            TrendingOut(
                repository_id=r.repository_id,
                full_name=r.full_name,
                language=r.language,
                description=r.description,
                html_url=r.html_url,
                stars_count=r.stars_count,
                stars_delta_7d=r.stars_delta_7d,
                stars_delta_30d=r.stars_delta_30d,
                engagement_score=r.engagement_score,
            )
            for r in rows
        ],
        "meta": {"days": days, "language": language, "total": len(rows)},
    }


@router.get("/weekly", response_model=ReportOut)
def get_weekly_report(
    language: Optional[str] = None,
    period: Optional[date] = None,
    db: Session = Depends(get_db),
):
    stmt = select(Report).where(Report.report_type == "weekly")
    if language:
        stmt = stmt.where(Report.language == language.lower())
    if period:
        stmt = stmt.where(Report.period_start == period)
    else:
        stmt = stmt.order_by(Report.period_start.desc())

    report = db.scalar(stmt.limit(1))
    if not report:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="No weekly report found.")
    return ReportOut.model_validate(report)


@router.get("/monthly", response_model=ReportOut)
def get_monthly_report(
    language: Optional[str] = None,
    period: Optional[date] = None,
    db: Session = Depends(get_db),
):
    stmt = select(Report).where(Report.report_type == "monthly")
    if language:
        stmt = stmt.where(Report.language == language.lower())
    if period:
        stmt = stmt.where(Report.period_start == period)
    else:
        stmt = stmt.order_by(Report.period_start.desc())

    report = db.scalar(stmt.limit(1))
    if not report:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="No monthly report found.")
    return ReportOut.model_validate(report)
