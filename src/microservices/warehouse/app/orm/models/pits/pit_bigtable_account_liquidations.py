from sqlalchemy import Column, Text, Float, text
from clickhouse_sqlalchemy import engines
from clickhouse_sqlalchemy.types.common import DateTime, UUID, Nullable
from sqlalchemy.ext.declarative import declared_attr
from fastapi_utils.camelcase import camel2snake

from app.orm.base.main import Base
from app.orm.cfg.settings import ORMSettings


class pitBigTableAccountLiquidations(Base):

    @declared_attr
    def __tablename__(cls) -> str:
        return camel2snake(cls.__name__)

    @declared_attr
    def __table_args__(cls):
        return engines.MergeTree(order_by=['pit_bigtable_account_liquidation_uuid']), {'schema': ORMSettings.DB_NAME}

    pit_bigtable_account_liquidation_uuid = Column(UUID, primary_key=True, server_default=text("generateUUIDv4()"))

    h_label_name = Column(Text)
    h_exchange_name = Column(Text)
    h_ticker_name = Column(Text)

    pit_amt = Column(Nullable(Float))
    pit_entry_price = Column(Nullable(Float))
    pit_liquidation_price = Column(Nullable(Float))
    pit_current_price = Column(Nullable(Float))
    pit_side = Column(Nullable(Text))
    pit_leverage = Column(Nullable(Float))
    pit_un_pnl = Column(Nullable(Float))

    pit_ts = Column(DateTime)
