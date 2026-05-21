import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

from collector.pipeline import run_full_collection
from config.settings import settings

logger = logging.getLogger("meridian.scheduler")


def start():
    scheduler = BlockingScheduler(timezone="UTC")
    scheduler.add_job(
        run_full_collection,
        trigger=IntervalTrigger(hours=settings.collect_interval_hours),
        id="full_collection",
        name="GitHub full collection",
        replace_existing=True,
        max_instances=1,
    )

    logger.info(
        "Scheduler started. Collection interval: every %d hours. Languages: %s",
        settings.collect_interval_hours,
        ", ".join(settings.languages),
    )

    # Run immediately on startup so the first collection doesn't wait
    logger.info("Running initial collection on startup...")
    try:
        run_full_collection()
    except Exception as exc:
        logger.error("Initial collection failed: %s", exc)

    scheduler.start()


if __name__ == "__main__":
    from config.logger import setup_logging
    setup_logging("meridian.scheduler")
    start()
