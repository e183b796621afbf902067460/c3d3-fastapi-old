from src.funds.orm.cfg.engine import ORMSettings
from src.funds.orm.base.main import Base

from sqlalchemy_utils import database_exists, drop_database, create_database


if __name__ == '__main__':
    ENGINE = ORMSettings.get_engine()
    URI = ORMSettings.get_uri()

    if database_exists(URI):
        drop_database(URI)
    create_database(URI)
    Base.metadata.create_all(ENGINE)
