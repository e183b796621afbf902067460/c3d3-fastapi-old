import pytest
from sqlalchemy.orm import Session
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy_utils import database_exists, drop_database, create_database

from typing import Generator, Any
import os
from urllib.parse import quote_plus

from src.orm.base.main import Base
from src.orm.cfg.engine import ORMSettings
from src.cfg.settings import settings
from src.funds.app.router import router as funds_flow_router
from src.instruments.app.router import router as instruments_flow_router


class TestORMSettings(ORMSettings):
    DB_ADDRESS = os.getenv('DB_ADDRESS', '')
    DB_USER = os.getenv('DB_USER', '')
    DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD', ''))
    DB_NAME = os.getenv('DB_NAME', '')

    DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}/{DB_NAME}'


def _startapp() -> FastAPI:
    _app: FastAPI = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f'{settings.API_V1}/openapi.json'
    )
    _app.include_router(funds_flow_router, prefix=settings.API_V1)
    _app.include_router(instruments_flow_router, prefix=settings.API_V1)
    return _app


@pytest.fixture(scope='function')
def environment() -> Generator[FastAPI, Any, None]:
    URI = TestORMSettings.get_uri()
    ENGINE = TestORMSettings.get_engine()
    if database_exists(URI):
        drop_database(URI)
    create_database(URI)
    Base.metadata.create_all(ENGINE)
    _app: FastAPI = _startapp()
    yield _app
    Base.metadata.drop_all(ENGINE)


@pytest.fixture(scope='function')
def client(environment) -> Generator[TestClient, Any, None]:

    def _session() -> Generator[Session, Any, None]:
        try:
            yield TestORMSettings.get_session()
        finally:
            pass

    environment.dependency_overrides[ORMSettings.get_session] = _session
    with TestClient(environment) as client:
        yield client
