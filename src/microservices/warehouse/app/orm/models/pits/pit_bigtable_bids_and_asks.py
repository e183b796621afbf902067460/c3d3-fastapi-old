from sqlalchemy import Column, Text, Float, text
from clickhouse_sqlalchemy import engines
from clickhouse_sqlalchemy.types.common import DateTime, UUID, Nullable
from sqlalchemy.ext.declarative import declared_attr
from fastapi_utils.camelcase import camel2snake

from app.orm.base.main import Base
from app.orm.cfg.settings import ORMSettings


class pitBigTableBidsAndAsks(Base):

    @declared_attr
    def __tablename__(cls) -> str:
        return camel2snake(cls.__name__)

    @declared_attr
    def __table_args__(cls):
        return engines.MergeTree(order_by=['pit_bigtable_bid_and_ask_uuid']), {'schema': ORMSettings.DB_NAME}

    pit_bigtable_bid_and_ask_uuid = Column(UUID, primary_key=True, server_default=text("generateUUIDv4()"))

    h_pool_address = Column(Text)
    h_protocol_name = Column(Text)
    h_network_name = Column(Text)
    h_native_chain_token = Column(Text)

    pit_symbol = Column(Nullable(Text))
    pit_bid = Column(Nullable(Float))
    pit_ask = Column(Nullable(Float))
    pit_price = Column(Nullable(Float))
    pit_sender = Column(Nullable(Text))
    pit_amount0 = Column(Nullable(Float))
    pit_amount1 = Column(Nullable(Float))
    pit_gas_used = Column(Nullable(Float))
    pit_effective_gas_price = Column(Nullable(Float))
    pit_gas_symbol = Column(Nullable(Text))
    pit_gas_price = Column(Nullable(Float))
    pit_index_position_in_the_block = Column(Nullable(Float))
    pit_tx_hash = Column(Nullable(Text))

    pit_ts = Column(DateTime)
