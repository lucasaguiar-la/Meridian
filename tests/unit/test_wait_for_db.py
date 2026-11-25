from unittest.mock import patch

from collector import wait_for_db


def test_returns_true_when_at_head():
    with patch.object(wait_for_db, "_expected_head", return_value="002"), patch.object(
        wait_for_db, "_current_revision", return_value="002"
    ):
        assert wait_for_db.wait_for_migrations(engine=object(), timeout_s=1, interval_s=0)


def test_waits_until_head_is_reached():
    revisions = iter([None, "001", "002"])
    with patch.object(wait_for_db, "_expected_head", return_value="002"), patch.object(
        wait_for_db, "_current_revision", side_effect=lambda _e: next(revisions)
    ):
        assert wait_for_db.wait_for_migrations(engine=object(), timeout_s=5, interval_s=0)


def test_tolerates_connection_errors_then_times_out():
    with patch.object(wait_for_db, "_expected_head", return_value="002"), patch.object(
        wait_for_db, "_current_revision", side_effect=RuntimeError("db down")
    ):
        assert not wait_for_db.wait_for_migrations(
            engine=object(), timeout_s=0.05, interval_s=0.01
        )


def test_expected_head_matches_repo_migrations():
    assert wait_for_db._expected_head() == "002"
