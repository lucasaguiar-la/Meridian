import logging
from typing import Optional

import requests

from config.settings import settings

logger = logging.getLogger("meridian.collector")

ADZUNA_API_BASE = "https://api.adzuna.com/v1/api/jobs"


class AdzunaConfigError(Exception):
    """Raised when Adzuna credentials are missing."""


class AdzunaClient:
    def __init__(
        self,
        app_id: Optional[str] = None,
        app_key: Optional[str] = None,
        country: Optional[str] = None,
    ):
        self._app_id = app_id or settings.adzuna_app_id
        self._app_key = app_key or settings.adzuna_app_key
        self._country = country or settings.adzuna_country
        self._session = requests.Session()

    def count_job_postings(self, keyword: str) -> int:
        """Returns the total number of open postings matching the keyword.

        Uses results_per_page=1 because Adzuna's search response includes the
        total match `count` regardless of page size, so a single lightweight
        call is enough to get an aggregate figure for a language.
        """
        if not self._app_id or not self._app_key:
            raise AdzunaConfigError(
                "Adzuna credentials are not configured (ADZUNA_APP_ID/ADZUNA_APP_KEY)."
            )

        url = f"{ADZUNA_API_BASE}/{self._country}/search/1"
        params = {
            "app_id": self._app_id,
            "app_key": self._app_key,
            "results_per_page": 1,
            "what": keyword,
            "content-type": "application/json",
        }
        response = self._session.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        return int(data.get("count", 0))
