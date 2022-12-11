import pytest
from sqlalchemy_utils import database_exists, drop_database, create_database

from src.orm.cfg.engine import ORMSettings
from src.orm.base.main import Base


URI = ORMSettings.get_uri()
ENGINE = ORMSettings.get_engine()


@pytest.fixture(scope='session', autouse=True)
def run():
    if database_exists(URI):
        drop_database(URI)
    create_database(URI)
    Base.metadata.create_all(ENGINE)


def test(run):
    assert database_exists(URI)
