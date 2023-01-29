from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declared_attr
from fastapi_utils.camelcase import camel2snake

from app.orm.base.main import Base


class lAddressesChainsProtocolsSpecifications(Base):

    @declared_attr
    def __tablename__(cls) -> str:
        return camel2snake(cls.__name__)

    l_address_chain_protocol_specification_id = Column(Integer, primary_key=True)
    l_address_chain_id = Column(Integer, ForeignKey('l_addresses_chains.l_address_chain_id'), nullable=False)
    l_protocol_specification_id = Column(Integer, ForeignKey('l_protocols_specifications.l_protocol_specification_id'), nullable=False)
