from sqlalchemy import Column, Integer, ForeignKey, Text

from src.orm.base.main import Base


class LinkAddressesProtocolsCategoriesChains(Base):

    __tablename__ = 'l_addresses_protocols_categories_chains'
    __table_args__ = {
        'comment': "Protocol's contracts"
    }

    l_address_protocol_category_chain_id = Column(Integer, primary_key=True)
    l_protocol_category_chain_id = Column(Integer, ForeignKey('l_protocols_categories_chains.l_protocol_category_chain_id'), nullable=False)
    l_address_chain_id = Column(Integer, ForeignKey('l_addresses_chains.l_address_chain_id'), nullable=False)
