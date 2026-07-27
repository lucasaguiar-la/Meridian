from typing import Optional, Literal
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy import select, func, text
from sqlalchemy.orm import Session

from api.dependencies import get_db
from api.schemas.market import LanguageMarketOut, MarketSnapshotOut
from api.schemas.repository import RepositoryOut, RepositoryListOut, RepositoryListMeta, SnapshotOut
from db.models import JobMarketSnapshot, Repository, RepositorySnapshot

router = APIRouter(prefix="/languages", tags=["languages"])


@router.get("")
def list_languages(db: Session = Depends(get_db)) -> dict:
    rows = db.execute(
        select(Repository.language, func.count(Repository.id).label("count"))
        .where(Repository.language.isnot(None))
        .group_by(Repository.language)
        .order_by(func.count(Repository.id).desc())
    ).all()
    return {
        "data": [{"language": r.language, "repository_count": r.count} for r in rows]
    }


@router.get("/{language}/ranking", response_model=RepositoryListOut)
def language_ranking(
    language: str,
    metric: Literal["stars", "engagement", "growth"] = "stars",
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    lang = language.lower()

    if metric == "stars":
        order_col = text("s.stars_count DESC NULLS LAST")
    elif metric == "engagement":
        order_col = text("s.engagement_score DESC NULLS LAST")
    else:
        order_col = text("s.stars_delta_30d DESC NULLS LAST")

    # Latest snapshot per repository using a subquery
    latest_subq = (
        select(
            RepositorySnapshot.repository_id,
            func.max(RepositorySnapshot.snapshot_date).label("max_date"),
        )
        .group_by(RepositorySnapshot.repository_id)
        .subquery("latest")
    )

    stmt = (
        select(Repository, RepositorySnapshot)
        .join(
            latest_subq,
            Repository.id == latest_subq.c.repository_id,
        )
        .join(
            RepositorySnapshot,
            (RepositorySnapshot.repository_id == latest_subq.c.repository_id)
            & (RepositorySnapshot.snapshot_date == latest_subq.c.max_date),
        )
        .where(func.lower(Repository.language) == lang)
        .order_by(order_col)
        .offset(offset)
        .limit(limit)
    )

    count_stmt = (
        select(func.count(Repository.id))
        .join(latest_subq, Repository.id == latest_subq.c.repository_id)
        .where(func.lower(Repository.language) == lang)
    )

    rows = db.execute(stmt).all()
    total = db.scalar(count_stmt) or 0

    if not rows and offset == 0:
        raise HTTPException(status_code=404, detail=f"No data found for language: {language}")

    items = []
    for repo, snapshot in rows:
        repo_out = RepositoryOut.model_validate(repo)
        repo_out.latest_snapshot = SnapshotOut.model_validate(snapshot)
        items.append(repo_out)

    return RepositoryListOut(
        data=items,
        meta=RepositoryListMeta(total=total, language=lang, limit=limit, offset=offset),
    )


@router.get("/{language}/market", response_model=LanguageMarketOut)
def language_market(language: str, db: Session = Depends(get_db)):
    """Latest job market snapshot(s) for a language, one per collected source (e.g. Adzuna)."""
    lang = language.lower()

    latest_subq = (
        select(
            JobMarketSnapshot.source,
            func.max(JobMarketSnapshot.snapshot_date).label("max_date"),
        )
        .where(func.lower(JobMarketSnapshot.language) == lang)
        .group_by(JobMarketSnapshot.source)
        .subquery("latest_market")
    )

    stmt = (
        select(JobMarketSnapshot)
        .join(
            latest_subq,
            (JobMarketSnapshot.source == latest_subq.c.source)
            & (JobMarketSnapshot.snapshot_date == latest_subq.c.max_date),
        )
        .where(func.lower(JobMarketSnapshot.language) == lang)
    )

    rows = db.scalars(stmt).all()
    if not rows:
        raise HTTPException(
            status_code=404, detail=f"No market data found for language: {language}"
        )

    return LanguageMarketOut(
        language=lang,
        data=[MarketSnapshotOut.model_validate(r) for r in rows],
    )
