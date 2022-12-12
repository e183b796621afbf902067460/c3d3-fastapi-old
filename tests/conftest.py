import pytest
from sqlalchemy.orm import Session, sessionmaker
from fastapi import FastAPI, status, HTTPException
from fastapi.testclient import TestClient
from sqlalchemy_utils import database_exists, drop_database, create_database

from typing import Generator, Any
import os
from urllib.parse import quote_plus
import json

from src.orm.base.main import Base
from src.orm.cfg.engine import ORMSettings
from src.cfg.settings import settings
from src.funds.app.router import router as funds_flow_router
from src.instruments.app.router import router as instruments_flow_router


def _create_authorization_header(client: TestClient, username: str, password: str):
    oauth2_ = {
        "username": username,
        "password": password
    }
    header = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = client.post(f'{settings.API_V1}/funds/labels/sign-in', data=oauth2_, headers=header)

    if response.status_code == status.HTTP_400_BAD_REQUEST:
        _ = client.post(f'{settings.API_V1}/funds/labels/sign-up', content=json.dumps(oauth2_))
        response = client.post(f'{settings.API_V1}/funds/labels/sign-in', data=oauth2_, headers=header)
        return {"Authorization": f"Bearer {response.json()['access_token']}"}
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


TEST_USERNAME: str = 'DEFI_MANAGEMENT_USERNAME'
TEST_PASSWORD: str = 'DEFI_MANAGEMENT_PASSWORD'

def _get_authorization_header(client: TestClient, username: str = TEST_USERNAME, password: str = TEST_PASSWORD):
    return _create_authorization_header(client=client, username=username, password=password)


class TestORMSettings(ORMSettings):
    DB_ADDRESS = os.getenv('DB_ADDRESS', 'localhost')
    DB_USER = os.getenv('DB_USER', 'username')
    DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD', '111222'))
    DB_NAME = os.getenv('DB_NAME', 'funds')

    DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}/{DB_NAME}'

    @classmethod
    def get_session(cls) -> sessionmaker:
        return sessionmaker(autocommit=False, autoflush=False, bind=cls.get_engine())


URI = TestORMSettings.get_uri()
ENGINE = TestORMSettings.get_engine()


def _startapp() -> FastAPI:
    _app: FastAPI = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f'{settings.API_V1}/openapi.json'
    )
    _app.include_router(funds_flow_router, prefix=settings.API_V1)
    _app.include_router(instruments_flow_router, prefix=settings.API_V1)
    return _app


@pytest.fixture(scope='module')
def environment() -> Generator[FastAPI, Any, None]:
    if database_exists(URI):
        drop_database(URI)
    create_database(URI)
    Base.metadata.create_all(ENGINE)
    _app: FastAPI = _startapp()
    yield _app
    Base.metadata.drop_all(ENGINE)


@pytest.fixture(scope="module")
def session(environment: FastAPI) -> Generator[Session, Any, None]:
    connection = TestORMSettings.get_engine().connect()
    transaction = connection.begin()
    session = TestORMSettings.get_session()(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope='module')
def client(environment, session) -> Generator[TestClient, Any, None]:

    def _session() -> Generator[Session, Any, None]:
        try:
            yield session
        finally:
            pass

    environment.dependency_overrides[ORMSettings.get_session] = _session
    with TestClient(environment) as client:
        yield client


@pytest.fixture(scope='module')
def jwt_token(client):
    return _get_authorization_header(client=client)