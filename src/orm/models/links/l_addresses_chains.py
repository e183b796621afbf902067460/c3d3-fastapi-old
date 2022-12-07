from sqlalchemy import Column, Integer, ForeignKey, Text

from src.orm.base.main import Base


class LinkAddressesChains(Base):

    __tablename__ = 'l_addresses_chains'
    __table_args__ = {
        'comment': "Chain's Addresses"
    }

    l_address_chain_id = Column(Integer, primary_key=True)
    h_address_id = Column(Integer, ForeignKey('h_addresses.h_address_id'), nullable=False)
    h_chain_id = Column(Integer, ForeignKey('h_chains.h_chain_id'), nullable=False)

    l_address_chain_name = Column(Text)
