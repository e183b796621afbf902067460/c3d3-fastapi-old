from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr

from fastapi_utils.camelcase import camel2snake

from app.orm.base.main import Base


class hTickers(Base):

    @declared_attr
    def __tablename__(cls) -> str:
        return camel2snake(cls.__name__)

    h_ticker_id = Column(Integer, primary_key=True)
    h_ticker_name = Column(Text, nullable=False)
    h_ticker_load_ts = Column(DateTime, server_default=func.now(), nullable=False)
