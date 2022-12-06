from src.orm.cfg.engine import ORMSettings
from src.orm.base.main import Base

from sqlalchemy_utils import database_exists

if __name__ == '__main__':
    ENGINE = ORMSettings.get_engine()
    URI = ORMSettings.get_uri()

    if database_exists(URI):
        Base.metadata.drop_all(ENGINE)
