from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr
from fastapi_utils.camelcase import camel2snake

from app.orm.base.main import Base


class hChains(Base):

    @declared_attr
    def __tablename__(cls) -> str:
        return camel2snake(cls.__name__)

    h_chain_id = Column(Integer, primary_key=True)

    h_network_name = Column(Text, nullable=False)
    h_native_chain_token = Column(Text, nullable=False)
    h_network_rpc_node = Column(Text, nullable=False)
    h_network_block_limit = Column(Integer, nullable=False)
    h_network_uri = Column(Text, nullable=False)
    h_network_api_key = Column(Text, nullable=False)

    h_network_load_ts = Column(DateTime, server_default=func.now(), nullable=False)
