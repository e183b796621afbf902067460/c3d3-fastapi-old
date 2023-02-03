from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr
from fastapi_utils.camelcase import camel2snake

from app.orm.base.main import Base


class lTokensOnWallets(Base):

    @declared_attr
    def __tablename__(cls) -> str:
        return camel2snake(cls.__name__)

    l_token_on_wallet_id = Column(Integer, primary_key=True)

    l_address_chain_id = Column(Integer, ForeignKey('l_addresses_chains.l_address_chain_id'), nullable=False)
    l_address_chain_label_id = Column(Integer, ForeignKey('l_addresses_chains_labels.l_address_chain_label_id'), nullable=False)
    l_token_on_wallet_load_ts = Column(DateTime, server_default=func.now(), nullable=False)
