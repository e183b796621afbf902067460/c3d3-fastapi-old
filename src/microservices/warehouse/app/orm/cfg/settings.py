from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

import os
from urllib.parse import quote_plus


class ORMSettings(object):
    DB_ADDRESS = os.getenv('CLICKHOUSE_HOST', '')
    DB_USER = os.getenv('CLICKHOUSE_USER', '')
    DB_PASSWORD = quote_plus(os.getenv('CLICKHOUSE_PASSWORD', ''))
    DB_NAME = os.getenv('CLICKHOUSE_DB', '')

    DB_URL = f'clickhouse://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}/{DB_NAME}'

    @classmethod
    def get_session(cls) -> Session:
        s = Session(cls.get_engine())
        try:
            yield s
        finally:
            s.close()

    @classmethod
    def get_engine(cls) -> Engine:
        return create_engine(cls.get_uri())

    @classmethod
    def get_uri(cls) -> str:
        return cls.DB_URL
