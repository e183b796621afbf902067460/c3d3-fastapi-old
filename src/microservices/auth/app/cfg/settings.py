from pydantic import BaseSettings
from decouple import config


class AppSettings(BaseSettings):

    API_V1: str = config('API_V1', cast=str, default='/api/v1')

    class Config:
        case_sensitive = True


settings: AppSettings = AppSettings()
