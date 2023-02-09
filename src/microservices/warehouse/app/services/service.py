from sqlalchemy.engine.base import Engine
from fastapi import Depends

from app.orm.cfg.settings import ORMSettings


class WarehouseService:

    def __init__(self, engine: Engine = Depends(ORMSettings.get_engine)):
        self._engine: Engine = engine

    def on_post__query(self, query: str):
        return self._engine.execute(query).fetchall()

