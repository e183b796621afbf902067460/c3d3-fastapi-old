from app.orm.cfg.engine import ORMSettings

from sqlalchemy_utils import database_exists, drop_database

if __name__ == '__main__':
    ENGINE = ORMSettings.get_engine()
    URI = ORMSettings.get_uri()

    if database_exists(URI):
        drop_database(URI)
