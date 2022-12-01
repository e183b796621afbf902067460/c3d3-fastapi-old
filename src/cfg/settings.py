from pydantic import BaseSettings


class AppSettings(BaseSettings):
    SERVER_HOST: str = ''
    SERVER_PORT: int = 0

    JWT_SECRET: str = 'asdf'
    JWT_ALGORITHM: str = 'HS256'
    JWT_EXPIRES: int = 3600


settings: AppSettings = AppSettings()
