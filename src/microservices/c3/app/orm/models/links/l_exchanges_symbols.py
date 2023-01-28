from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr

from fastapi_utils.camelcase import camel2snake

from app.orm.base.main import Base


class lExchangesSymbols(Base):

    @declared_attr
    def __tablename__(cls) -> str:
        return camel2snake(cls.__name__)

    l_exchange_symbol_id = Column(Integer, primary_key=True)
    h_exchange_id = Column(Integer, ForeignKey('h_exchanges.h_exchange_id'), nullable=False)
    h_symbol_id = Column(Integer, ForeignKey('h_symbols.h_symbol_id'), nullable=False)
    l_exchange_symbol_load_ts = Column(DateTime, server_default=func.now(), nullable=False)
