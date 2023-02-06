from pydantic import BaseSettings, AnyHttpUrl
from decouple import config


class AppSettings(BaseSettings):
    API_V1: str = config('API_V1', cast=str, default='/api/v1')

    AUTH_SERVICE_URL: str = 'http://auth-service:8000'
    C3_SERVICE_URL: str = 'http://c3-service:8000'
    D3_SERVICE_URL: str = 'http://d3-service:8000'

    JWT_FERNET_KEY: str = config('JWT_FERNET_KEY', cast=str)
    JWT_ALGORITHM: str = config('JWT_ALGORITHM', cast=str, default='HS256')
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = config('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', cast=int, default=60)

    class Config:
        case_sensitive = True


settings: AppSettings = AppSettings()
