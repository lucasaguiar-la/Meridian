import logging
import sys
from pythonjsonlogger import jsonlogger
from config.settings import settings


def setup_logging(service: str = "meridian") -> logging.Logger:
    logger = logging.getLogger(service)
    logger.setLevel(getattr(logging, settings.log_level.upper(), logging.INFO))

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = jsonlogger.JsonFormatter(
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%SZ",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # Suppress noisy third-party loggers
    for noisy in ("httpx", "httpcore", "urllib3", "sqlalchemy.engine"):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    return logger


logger = setup_logging()
