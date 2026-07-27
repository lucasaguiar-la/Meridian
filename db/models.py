from datetime import datetime, date
from typing import Optional
from sqlalchemy import (
    BigInteger, Integer, Float, String, Text, Boolean,
    DateTime, Date, ForeignKey, UniqueConstraint, Index, JSON,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Repository(Base):
    __tablename__ = "repositories"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)  # GitHub repo ID
    full_name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text)
    language: Mapped[Optional[str]] = mapped_column(String(100))
    html_url: Mapped[Optional[str]] = mapped_column(Text)
    owner_login: Mapped[Optional[str]] = mapped_column(String(100))
    is_fork: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    collected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    snapshots: Mapped[list["RepositorySnapshot"]] = relationship(
        back_populates="repository", cascade="all, delete-orphan"
    )
    ai_summaries: Mapped[list["AiSummary"]] = relationship(
        back_populates="repository", cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("ix_repositories_language", "language"),
    )


class RepositorySnapshot(Base):
    __tablename__ = "repository_snapshots"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    repository_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False, index=True
    )
    snapshot_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)

    stars_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    forks_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    watchers_count: Mapped[Optional[int]] = mapped_column(Integer)
    open_issues_count: Mapped[Optional[int]] = mapped_column(Integer)
    network_count: Mapped[Optional[int]] = mapped_column(Integer)
    subscribers_count: Mapped[Optional[int]] = mapped_column(Integer)

    engagement_score: Mapped[Optional[float]] = mapped_column(Float)
    stars_delta_7d: Mapped[Optional[int]] = mapped_column(Integer)
    stars_delta_30d: Mapped[Optional[int]] = mapped_column(Integer)

    repository: Mapped["Repository"] = relationship(back_populates="snapshots")

    __table_args__ = (
        UniqueConstraint("repository_id", "snapshot_date", name="uq_snapshot_per_day"),
        Index("ix_snapshots_repo_date", "repository_id", "snapshot_date"),
    )


class AiSummary(Base):
    __tablename__ = "ai_summaries"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    repository_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False
    )
    period_type: Mapped[str] = mapped_column(String(10), nullable=False)  # weekly | monthly
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    model_used: Mapped[Optional[str]] = mapped_column(String(100))
    tokens_used: Mapped[Optional[int]] = mapped_column(Integer)
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    repository: Mapped["Repository"] = relationship(back_populates="ai_summaries")

    __table_args__ = (
        UniqueConstraint(
            "repository_id", "period_type", "period_start",
            name="uq_ai_summary_per_period",
        ),
    )


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    report_type: Mapped[str] = mapped_column(String(10), nullable=False)  # weekly | monthly
    language: Mapped[Optional[str]] = mapped_column(String(100))
    period_start: Mapped[date] = mapped_column(Date, nullable=False)
    period_end: Mapped[date] = mapped_column(Date, nullable=False)
    content_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (
        UniqueConstraint(
            "report_type", "language", "period_start",
            name="uq_report_per_period",
        ),
    )


class CollectorRun(Base):
    """Tracks each collector execution for observability."""
    __tablename__ = "collector_runs"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    language: Mapped[Optional[str]] = mapped_column(String(100))
    repos_collected: Mapped[Optional[int]] = mapped_column(Integer)
    repos_updated: Mapped[Optional[int]] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(20), default="running")  # running | success | error
    error_message: Mapped[Optional[str]] = mapped_column(Text)
