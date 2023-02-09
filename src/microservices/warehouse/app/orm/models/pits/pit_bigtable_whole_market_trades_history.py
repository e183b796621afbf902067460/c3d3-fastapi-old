from sqlalchemy import Column, Text, Float, text
from clickhouse_sqlalchemy import engines
from clickhouse_sqlalchemy.types.common import DateTime, UUID, Nullable
from sqlalchemy.ext.declarative import declared_attr
from fastapi_utils.camelcase import camel2snake

from app.orm.base.main import Base
from app.orm.cfg.settings import ORMSettings


class pitBigTableWholeMarketTradesHistory(Base):

    @declared_attr
    def __tablename__(cls) -> str:
        return camel2snake(cls.__name__)

    @declared_attr
    def __table_args__(cls):
        return engines.MergeTree(order_by=['pit_bigtable_whole_market_trade_history_uuid']), {'schema': ORMSettings.DB_NAME}

    pit_bigtable_whole_market_trade_history_uuid = Column(UUID, primary_key=True, server_default=text("generateUUIDv4()"))

    h_exchange_name = Column(Text)
    h_ticker_name = Column(Text)

    pit_price = Column(Nullable(Float))
    pit_qty = Column(Nullable(Float))
    pit_side = Column(Nullable(Text))

    pit_ts = Column(DateTime)
