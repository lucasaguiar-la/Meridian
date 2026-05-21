import time
import logging
from typing import Optional
from datetime import datetime, timezone

import requests

from config.settings import settings

logger = logging.getLogger("meridian.collector")

GITHUB_API_BASE = "https://api.github.com"


class RateLimitError(Exception):
    pass


class GitHubClient:
    def __init__(self, token: Optional[str] = None):
        self._token = token or settings.github_token
        self._session = requests.Session()
        self._session.headers.update({
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        })
        if self._token:
            self._session.headers["Authorization"] = f"Bearer {self._token}"

    def _get(self, path: str, params: Optional[dict] = None) -> dict | list:
        url = f"{GITHUB_API_BASE}{path}"
        response = self._session.get(url, params=params, timeout=30)
        self._check_rate_limit(response)
        response.raise_for_status()
        return response.json()

    def _check_rate_limit(self, response: requests.Response) -> None:
        remaining = int(response.headers.get("X-RateLimit-Remaining", 1))
        reset_ts = int(response.headers.get("X-RateLimit-Reset", 0))

        if response.status_code == 403 and remaining == 0:
            wait_seconds = max(reset_ts - int(time.time()), 0) + 5
            logger.warning(
                "GitHub rate limit reached. Waiting %d seconds.", wait_seconds,
                extra={"reset_at": datetime.fromtimestamp(reset_ts, tz=timezone.utc).isoformat()},
            )
            time.sleep(wait_seconds)
            raise RateLimitError("Rate limit hit; caller should retry.")

        if remaining < 50:
            logger.info("GitHub rate limit low: %d requests remaining.", remaining)

    def search_repositories(self, language: str, per_page: int = 100, page: int = 1) -> dict:
        params = {
            "q": f"language:{language} stars:>50",
            "sort": "stars",
            "order": "desc",
            "per_page": min(per_page, 100),
            "page": page,
        }
        return self._get("/search/repositories", params=params)

    def get_repository(self, owner: str, repo: str) -> dict:
        return self._get(f"/repos/{owner}/{repo}")

    def get_rate_limit_status(self) -> dict:
        return self._get("/rate_limit")
