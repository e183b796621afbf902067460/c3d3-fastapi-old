from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr

from fastapi_utils.camelcase import camel2snake

from app.orm.base.main import Base


class lExchangesTickers(Base):

    @declared_attr
    def __tablename__(cls) -> str:
        return camel2snake(cls.__name__)

    l_exchange_ticker_id = Column(Integer, primary_key=True)
    h_exchange_id = Column(Integer, ForeignKey('h_exchanges.h_exchange_id'), nullable=False)
    h_ticker_id = Column(Integer, ForeignKey('h_tickers.h_ticker_id'), nullable=False)
    l_exchange_ticker_load_ts = Column(DateTime, server_default=func.now(), nullable=False)
