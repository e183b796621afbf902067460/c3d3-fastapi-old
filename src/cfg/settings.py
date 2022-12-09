from pydantic import BaseSettings, AnyHttpUrl
from decouple import config

from pathlib import Path
from typing import List
from functools import lru_cache


class AppSettings(BaseSettings):
    PROJECT_NAME: str = "DeFi Management"

    API_V1: str = '/api/v1'

    JWT_SECRET_KEY: str = config('JWT_SECRET_KEY', cast=str, default='!secret')
    JWT_REFRESH_SECRET_KEY: str = config('JWT_REFRESH_SECRET_KEY', cast=str, default='!refresh')
    JWT_ALGORITHM: str = 'HS256'

    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl]

    BASE_PATH = Path(__file__[:-15]).resolve()

    class Config:
        case_sensitive = True


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()


settings: AppSettings = get_settings()
