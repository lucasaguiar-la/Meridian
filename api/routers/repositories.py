from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from api.dependencies import get_db
from api.schemas.repository import RepositoryOut, SnapshotOut, RepositoryListOut, RepositoryListMeta
from db.models import Repository, RepositorySnapshot

router = APIRouter(prefix="/repositories", tags=["repositories"])


def _get_latest_snapshot(db: Session, repo_id: int) -> Optional[RepositorySnapshot]:
    return db.scalar(
        select(RepositorySnapshot)
        .where(RepositorySnapshot.repository_id == repo_id)
        .order_by(RepositorySnapshot.snapshot_date.desc())
        .limit(1)
    )


@router.get("/{repo_id}", response_model=RepositoryOut)
def get_repository(repo_id: int, db: Session = Depends(get_db)):
    repo = db.get(Repository, repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    out = RepositoryOut.model_validate(repo)
    snapshot = _get_latest_snapshot(db, repo_id)
    if snapshot:
        out.latest_snapshot = SnapshotOut.model_validate(snapshot)
    return out


@router.get("/{repo_id}/history")
def get_repository_history(
    repo_id: int,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
):
    repo = db.get(Repository, repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    from datetime import date, timedelta
    cutoff = date.today() - timedelta(days=days)
    snapshots = db.scalars(
        select(RepositorySnapshot)
        .where(
            RepositorySnapshot.repository_id == repo_id,
            RepositorySnapshot.snapshot_date >= cutoff,
        )
        .order_by(RepositorySnapshot.snapshot_date.asc())
    ).all()

    return {
        "repository_id": repo_id,
        "full_name": repo.full_name,
        "data": [SnapshotOut.model_validate(s) for s in snapshots],
    }


@router.get("/search/")
def search_repositories(
    q: str = Query(..., min_length=2),
    language: Optional[str] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    stmt = select(Repository).where(
        Repository.full_name.ilike(f"%{q}%")
        | Repository.description.ilike(f"%{q}%")
    )
    if language:
        stmt = stmt.where(func.lower(Repository.language) == language.lower())

    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    repos = db.scalars(stmt.offset(offset).limit(limit)).all()

    items = []
    for repo in repos:
        out = RepositoryOut.model_validate(repo)
        snapshot = _get_latest_snapshot(db, repo.id)
        if snapshot:
            out.latest_snapshot = SnapshotOut.model_validate(snapshot)
        items.append(out)

    return RepositoryListOut(
        data=items,
        meta=RepositoryListMeta(total=total, language=language, limit=limit, offset=offset),
    )
