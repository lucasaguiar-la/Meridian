import logging
from typing import Optional

import requests

from config.settings import settings

logger = logging.getLogger("meridian.collector")

ADZUNA_API_BASE = "https://api.adzuna.com/v1/api/jobs"
REMOTEOK_API_URL = "https://remoteok.com/api"

# Some language keywords are too ambiguous for a free-text/tag match:
# "go" matches "go-getter", "on the go", "go-to-market", etc. in Adzuna's
# descriptions/titles (11k+ vs ~200-300 for "golang"), and RemoteOK's own
# tags use "golang" rather than "go" too. Confirmed empirically against both
# live APIs. Everything else searched fine as-is.
LANGUAGE_KEYWORD_OVERRIDES = {
    "go": "golang",
}


class AdzunaConfigError(Exception):
    """Raised when Adzuna credentials are missing."""


class AdzunaClient:
    def __init__(
        self,
        app_id: Optional[str] = None,
        app_key: Optional[str] = None,
        country: Optional[str] = None,
    ):
        self._app_id = app_id if app_id is not None else settings.adzuna_app_id
        self._app_key = app_key if app_key is not None else settings.adzuna_app_key
        self._country = country if country is not None else settings.adzuna_country
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

        search_term = LANGUAGE_KEYWORD_OVERRIDES.get(keyword.lower(), keyword)
        url = f"{ADZUNA_API_BASE}/{self._country}/search/1"
        params = {
            "app_id": self._app_id,
            "app_key": self._app_key,
            "results_per_page": 1,
            "what": search_term,
            "content-type": "application/json",
        }
        response = self._session.get(url, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        return int(data.get("count", 0))


class RemoteOKClient:
    """Public RemoteOK job board API (https://remoteok.com/api), no auth required.

    Unlike Adzuna, RemoteOK has no per-keyword search endpoint: a single request
    returns a batch of current listings (the unauthenticated feed caps out around
    ~100 recent postings, not RemoteOK's full board), each already tagged with
    lowercase technology tags. Counting per language is done locally against that
    one fetched batch, so callers should fetch once per collection run and reuse
    it across languages instead of re-fetching per language. Given the small
    batch size, expect much lower counts than Adzuna for the same language.
    """

    def __init__(self):
        self._session = requests.Session()
        # RemoteOK's usage terms ask API consumers to identify themselves.
        self._session.headers.update(
            {"User-Agent": "Meridian (https://github.com/lucasaguiar-la/Meridian)"}
        )

    def fetch_listings(self) -> list[dict]:
        response = self._session.get(REMOTEOK_API_URL, timeout=30)
        response.raise_for_status()
        data = response.json()
        # The first element is a legal/attribution notice, not a job listing.
        return [item for item in data if isinstance(item, dict) and "tags" in item]

    @staticmethod
    def count_by_tag(listings: list[dict], keyword: str) -> int:
        kw = LANGUAGE_KEYWORD_OVERRIDES.get(keyword.lower(), keyword.lower())
        return sum(
            1
            for job in listings
            if kw in [str(tag).lower() for tag in job.get("tags", [])]
        )
