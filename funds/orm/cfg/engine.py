from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session
import os
from urllib.parse import quote_plus

from head.interfaces.db.settings.interface import ISettings


class ORMSettings(ISettings):
    DB_ADDRESS = os.getenv('DB_ADDRESS', '')
    DB_USER = os.getenv('DB_USER', '')
    DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD', ''))
    DB_NAME = os.getenv('DB_NAME', '')

    DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}/{DB_NAME}'

    @classmethod
    def get_session(cls):
        return Session(cls.get_engine())

    @classmethod
    def get_engine(cls) -> Engine:
        return create_engine(cls.get_uri())

    @classmethod
    def get_uri(cls) -> str:
        return cls.DB_URL


settings: ORMSettings = ORMSettings()
