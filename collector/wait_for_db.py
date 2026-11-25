import logging
import time
from pathlib import Path

from alembic.config import Config
from alembic.runtime.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy.engine import Engine

logger = logging.getLogger("meridian.collector")

_ROOT = Path(__file__).resolve().parent.parent


def _expected_head() -> str:
    cfg = Config(str(_ROOT / "alembic.ini"))
    # script_location in alembic.ini is relative to the cwd; make it absolute.
    cfg.set_main_option("script_location", str(_ROOT / "db" / "migrations"))
    return ScriptDirectory.from_config(cfg).get_current_head()


def _current_revision(engine: Engine):
    with engine.connect() as conn:
        return MigrationContext.configure(conn).get_current_revision()


def wait_for_migrations(
    engine: Engine = None,
    timeout_s: float = 300,
    interval_s: float = 5,
) -> bool:
    """Block until the database is at the Alembic head revision.

    Returns True once migrated, False if `timeout_s` elapses first. Connection
    errors and a missing `alembic_version` table count as "not ready yet".
    """
    if engine is None:
        from db.session import engine as default_engine

        engine = default_engine

    head = _expected_head()
    deadline = time.monotonic() + timeout_s

    while True:
        try:
            current = _current_revision(engine)
            if current == head:
                logger.info("Database is at migration head (%s).", head)
                return True
            logger.info(
                "Waiting for migrations (current=%s, expected=%s)...", current, head
            )
        except Exception as exc:
            logger.info("Database not ready yet (%s); retrying...", exc)

        if time.monotonic() >= deadline:
            logger.error("Timed out after %ss waiting for migrations.", timeout_s)
            return False
        time.sleep(interval_s)
