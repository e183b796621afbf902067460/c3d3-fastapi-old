from sqlalchemy import Column, Text, Float, text
from clickhouse_sqlalchemy import engines
from clickhouse_sqlalchemy.types.common import DateTime, UUID, Nullable
from sqlalchemy.ext.declarative import declared_attr
from fastapi_utils.camelcase import camel2snake

from app.orm.base.main import Base
from app.orm.cfg.settings import ORMSettings


class pitBigTableHedgeToBorrows(Base):

    @declared_attr
    def __tablename__(cls) -> str:
        return camel2snake(cls.__name__)

    @declared_attr
    def __table_args__(cls):
        return engines.MergeTree(order_by=['pit_bigtable_hedge_to_borrows_uuid']), {'schema': ORMSettings.DB_NAME}

    pit_bigtable_hedge_to_borrows_uuid = Column(UUID, primary_key=True, server_default=text("generateUUIDv4()"))

    h_wallet_address = Column(Text)
    h_label_name = Column(Text)
    h_protocol_name = Column(Text)
    h_token_address = Column(Text)
    h_network_name = Column(Text)

    pit_symbol = Column(Nullable(Text))
    pit_price = Column(Nullable(Float))
    pit_qty = Column(Nullable(Float))
    pit_health_factor = Column(Nullable(Float))

    pit_ts = Column(DateTime)
