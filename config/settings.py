from pydantic_settings import BaseSettings


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
    # Comma-separated list of languages (kept as a plain str, not List[str]:
    # pydantic-settings tries to JSON-decode complex types read from env/.env,
    # which breaks a plain comma-separated value like "python,javascript,...").
    languages: str = "python,javascript,typescript,go,rust,java,c++,c#,kotlin,swift"
    repos_per_language: int = 100

    # Job market (Adzuna API, https://developer.adzuna.com; RemoteOK, no auth needed)
    adzuna_app_id: str = ""
    adzuna_app_key: str = ""
    adzuna_country: str = "br"
    market_collect_interval_hours: int = 24

    # App
    log_level: str = "INFO"
    app_version: str = "1.0.0"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        # .env carries docker-compose-only keys (POSTGRES_DB/USER/PASSWORD) that
        # this model doesn't declare; without this they'd fail as forbidden extras.
        extra = "ignore"


settings = Settings()
