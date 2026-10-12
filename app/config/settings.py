from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "release-notifier"
    app_timezone: str = "UTC"
    database_url: str = "sqlite://data/release_notifier.db"

    github_token: str | None = None
    github_api_base_url: str = "https://api.github.com"

    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    smtp_use_tls: bool = True
    email_from: str | None = None

    telegram_bot_token: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()

# Ensure the SQLite directory exists.
Path("data").mkdir(exist_ok=True)
