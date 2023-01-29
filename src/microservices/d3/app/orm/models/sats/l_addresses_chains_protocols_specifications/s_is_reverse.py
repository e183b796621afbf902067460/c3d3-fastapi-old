from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declared_attr
from fastapi_utils.camelcase import camel2snake

from app.orm.base.main import Base


class sIsReverse(Base):

    @declared_attr
    def __tablename__(cls) -> str:
        return camel2snake(cls.__name__)

    s_is_reverse_id = Column(Integer, primary_key=True)
    l_address_chain_protocol_specification_id = Column(Integer, ForeignKey('l_addresses_chains_protocols_specifications.l_address_chain_protocol_specification_id'), nullable=False)
    s_is_reverse = Column(Boolean, nullable=True)
