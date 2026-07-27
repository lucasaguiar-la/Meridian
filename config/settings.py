from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://meridian:changeme@localhost:5432/meridian"

    # GitHub API
    github_token: str = ""

    # Gemini AI (optional)
    ai_enabled: bool = False
    gemini_api_key: str = ""
    ai_top_repos_per_language: int = 20

    # Collector
    collect_interval_hours: int = 6
    languages: List[str] = ["python", "javascript", "typescript", "go", "rust", "java", "c++", "c#", "kotlin", "swift"]
    repos_per_language: int = 100

    # Job market (Adzuna API, https://developer.adzuna.com)
    adzuna_app_id: str = ""
    adzuna_app_key: str = ""
    adzuna_country: str = "br"

    # App
    log_level: str = "INFO"
    app_version: str = "1.0.0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
