from datetime import date, timedelta

from core.metrics import get_stars_delta
from db.models import Repository, RepositorySnapshot


def _make_repo(db_session, repo_id=1):
    repo = Repository(id=repo_id, full_name="octocat/hello-world", name="hello-world")
    db_session.add(repo)
    db_session.commit()
    return repo


def _add_snapshot(db_session, repo_id, snapshot_date, stars_count):
    next_id = (db_session.query(RepositorySnapshot).count()) + 1
    snapshot = RepositorySnapshot(
        id=next_id,
        repository_id=repo_id,
        snapshot_date=snapshot_date,
        stars_count=stars_count,
    )
    db_session.add(snapshot)
    db_session.commit()


def test_no_snapshots_returns_none(db_session):
    _make_repo(db_session)
    assert get_stars_delta(db_session, repository_id=1, days=7) is None


def test_single_snapshot_returns_zero_delta(db_session):
    _make_repo(db_session)
    _add_snapshot(db_session, 1, date.today(), stars_count=100)
    assert get_stars_delta(db_session, repository_id=1, days=7) == 0


def test_delta_uses_oldest_snapshot_within_window(db_session):
    _make_repo(db_session)
    today = date.today()
    _add_snapshot(db_session, 1, today - timedelta(days=30), stars_count=10)
    _add_snapshot(db_session, 1, today - timedelta(days=5), stars_count=50)
    _add_snapshot(db_session, 1, today, stars_count=80)

    assert get_stars_delta(db_session, repository_id=1, days=7) == 30
