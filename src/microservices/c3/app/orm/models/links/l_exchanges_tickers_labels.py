from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr

from fastapi_utils.camelcase import camel2snake

from app.orm.base.main import Base


class lExchangesTickersLabels(Base):

    @declared_attr
    def __tablename__(cls) -> str:
        return camel2snake(cls.__name__)

    l_exchange_ticker_label_id = Column(Integer, primary_key=True)
    h_label_id = Column(Integer, ForeignKey('h_labels.h_label_id'), nullable=False)
    l_exchange_ticker_id = Column(Integer, ForeignKey('l_exchanges_tickers.l_exchange_ticker_id'), nullable=False)
    l_exchange_ticker_label_load_ts = Column(DateTime, server_default=func.now(), nullable=False)
