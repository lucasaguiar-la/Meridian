from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator, model_validator
from typing import List, Union, Optional


class Settings(BaseSettings):
    # Database
    database_url: Optional[str] = None
    
    # These are used to build database_url if not provided
    postgres_user: str = "meridian"
    postgres_password: str = "changeme"
    postgres_db: str = "meridian"
    postgres_host: str = "localhost"
    postgres_port: str = "5434"

    @model_validator(mode="after")
    def assemble_database_url(self) -> "Settings":
        if not self.database_url:
            self.database_url = (
                f"postgresql://{self.postgres_user}:{self.postgres_password}@"
                f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
            )
        return self

    # GitHub API
    github_token: str = ""

    # Gemini AI (optional)
    ai_enabled: bool = False
    gemini_api_key: str = ""
    ai_top_repos_per_language: int = 20

    # Collector
    collect_interval_hours: int = 6
    languages: Union[str, List[str]] = ["python", "javascript", "typescript", "go", "rust"]
    repos_per_language: int = 100

    @field_validator("languages", mode="before")
    @classmethod
    def parse_languages(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            return [lang.strip() for lang in v.split(",")]
        return v

    # App
    log_level: str = "INFO"
    app_version: str = "1.0.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore" # Ignore extra fields like GITHUB_TOKEN if we don't want to map them all
    )


settings = Settings()
