import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from api.routers import languages, repositories, reports
from config.logger import setup_logging
from config.settings import settings
from db.session import engine

setup_logging("meridian.api")
logger = logging.getLogger("meridian.api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Meridian API starting up. Version: %s", settings.app_version)
    yield
    logger.info("Meridian API shutting down.")


app = FastAPI(
    title="Meridian API",
    description="GitHub repository insights platform",
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

app.include_router(languages.router)
app.include_router(repositories.router)
app.include_router(reports.router)


@app.get("/health", tags=["system"])
def health_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as exc:
        logger.error("Health check: DB connection failed: %s", exc)
        db_status = "unavailable"

    return {
        "status": "ok" if db_status == "connected" else "degraded",
        "db": db_status,
        "version": settings.app_version,
    }


@app.get("/collector/status", tags=["system"])
def collector_status():
    from sqlalchemy.orm import Session
    from db.session import SessionLocal
    from db.models import CollectorRun
    from sqlalchemy import select

    db: Session = SessionLocal()
    try:
        last_run = db.scalar(
            select(CollectorRun)
            .order_by(CollectorRun.started_at.desc())
            .limit(1)
        )
        if not last_run:
            return {"last_run": None, "status": "never_run"}
        return {
            "last_run": {
                "started_at": last_run.started_at,
                "finished_at": last_run.finished_at,
                "language": last_run.language,
                "status": last_run.status,
                "repos_collected": last_run.repos_collected,
            }
        }
    finally:
        db.close()
