"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-05-21

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "repositories",
        sa.Column("id", sa.BigInteger(), nullable=False),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("language", sa.String(100), nullable=True),
        sa.Column("html_url", sa.Text(), nullable=True),
        sa.Column("owner_login", sa.String(100), nullable=True),
        sa.Column("is_fork", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("collected_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("full_name"),
    )
    op.create_index("ix_repositories_language", "repositories", ["language"])

    op.create_table(
        "repository_snapshots",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=True), nullable=False),
        sa.Column("repository_id", sa.BigInteger(), nullable=False),
        sa.Column("snapshot_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("snapshot_date", sa.Date(), nullable=False),
        sa.Column("stars_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("forks_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("watchers_count", sa.Integer(), nullable=True),
        sa.Column("open_issues_count", sa.Integer(), nullable=True),
        sa.Column("network_count", sa.Integer(), nullable=True),
        sa.Column("subscribers_count", sa.Integer(), nullable=True),
        sa.Column("engagement_score", sa.Float(), nullable=True),
        sa.Column("stars_delta_7d", sa.Integer(), nullable=True),
        sa.Column("stars_delta_30d", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("repository_id", "snapshot_date", name="uq_snapshot_per_day"),
    )
    op.create_index("ix_snapshots_repo_date", "repository_snapshots", ["repository_id", "snapshot_date"])

    op.create_table(
        "ai_summaries",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=True), nullable=False),
        sa.Column("repository_id", sa.BigInteger(), nullable=False),
        sa.Column("period_type", sa.String(10), nullable=False),
        sa.Column("period_start", sa.Date(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("model_used", sa.String(100), nullable=True),
        sa.Column("tokens_used", sa.Integer(), nullable=True),
        sa.Column("generated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.ForeignKeyConstraint(["repository_id"], ["repositories.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("repository_id", "period_type", "period_start", name="uq_ai_summary_per_period"),
    )

    op.create_table(
        "reports",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=True), nullable=False),
        sa.Column("report_type", sa.String(10), nullable=False),
        sa.Column("language", sa.String(100), nullable=True),
        sa.Column("period_start", sa.Date(), nullable=False),
        sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("content_json", sa.JSON(), nullable=False),
        sa.Column("generated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("report_type", "language", "period_start", name="uq_report_per_period"),
    )

    op.create_table(
        "collector_runs",
        sa.Column("id", sa.BigInteger(), sa.Identity(always=True), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("language", sa.String(100), nullable=True),
        sa.Column("repos_collected", sa.Integer(), nullable=True),
        sa.Column("repos_updated", sa.Integer(), nullable=True),
        sa.Column("status", sa.String(20), server_default="running"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # View: latest snapshot per repository
    op.execute("""
        CREATE VIEW latest_snapshots AS
        SELECT DISTINCT ON (s.repository_id)
            s.*,
            r.full_name,
            r.name,
            r.language,
            r.description,
            r.html_url,
            r.owner_login,
            r.is_fork
        FROM repository_snapshots s
        JOIN repositories r ON r.id = s.repository_id
        ORDER BY s.repository_id, s.snapshot_date DESC
    """)


def downgrade() -> None:
    op.execute("DROP VIEW IF EXISTS latest_snapshots")
    op.drop_table("collector_runs")
    op.drop_table("reports")
    op.drop_table("ai_summaries")
    op.drop_table("repository_snapshots")
    op.drop_table("repositories")
