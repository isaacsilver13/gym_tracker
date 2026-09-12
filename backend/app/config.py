import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import dotenv_values

_DOTENV_PATH = Path(__file__).resolve().parents[2] / ".env"
_DEFAULT_DATABASE_URL = "sqlite:///./gym_tracker_dev.db"


def _setting(name: str, default: str) -> str:
    process_value = os.getenv(name)
    if process_value is not None and process_value.strip():
        return process_value

    file_value = dotenv_values(_DOTENV_PATH).get(name)
    return file_value if file_value is not None else default


@dataclass(frozen=True)
class Settings:
    app_env: str
    database_url: str
    session_secret: str


def load_settings() -> Settings:
    return Settings(
        app_env=_setting("APP_ENV", "development").strip().lower(),
        database_url=_setting("DATABASE_URL", _DEFAULT_DATABASE_URL),
        session_secret=_setting("SESSION_SECRET", "dev-only-insecure-secret"),
    )
