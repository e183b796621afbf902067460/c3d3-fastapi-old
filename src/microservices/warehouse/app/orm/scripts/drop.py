from app.orm.cfg.settings import ORMSettings
from app.orm.base.main import Base

from sqlalchemy_utils import database_exists

if __name__ == '__main__':
    ENGINE, URI = ORMSettings.get_engine(), ORMSettings.get_uri()

    if database_exists(URI):
        Base.metadata.drop_all(ENGINE)
