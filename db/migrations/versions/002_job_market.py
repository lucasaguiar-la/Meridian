"""job market snapshots

Revision ID: 002
Revises: 001
Create Date: 2026-07-27

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "job_market_snapshots",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=True), nullable=False),
        sa.Column("language", sa.String(100), nullable=False),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("snapshot_date", sa.Date(), nullable=False),
        sa.Column("open_positions_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("avg_salary", sa.Float(), nullable=True),
        sa.Column("collected_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("language", "source", "snapshot_date", name="uq_market_snapshot_per_day"),
    )
    op.create_index("ix_job_market_snapshots_language", "job_market_snapshots", ["language"])


def downgrade() -> None:
    op.drop_index("ix_job_market_snapshots_language", table_name="job_market_snapshots")
    op.drop_table("job_market_snapshots")
