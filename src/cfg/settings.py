from pydantic import BaseSettings


class AppSettings(BaseSettings):
    SERVER_HOST: str = '127.0.0.1'
    SERVER_PORT: int = 8080

    JWT_SECRET: str = '!settings'
    JWT_ALGORITHM: str = 'HS256'
    JWT_EXPIRES: int = 3600


settings: AppSettings = AppSettings()
