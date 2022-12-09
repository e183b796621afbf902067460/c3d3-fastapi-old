import pytest
from sqlalchemy_utils import database_exists, drop_database, create_database

from src.orm.cfg.engine import ORMSettings
from src.orm.base.main import Base


@pytest.fixture(scope='session', autouse=True)
def db_init():
    if database_exists(ORMSettings.get_uri()):
        drop_database(ORMSettings.get_uri())
    create_database(ORMSettings.get_uri())
    Base.metadata.create_all(ORMSettings.get_engine())
