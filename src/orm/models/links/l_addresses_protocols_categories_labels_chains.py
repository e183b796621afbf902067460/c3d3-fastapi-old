from sqlalchemy import Column, Integer, ForeignKey

from src.orm.base.main import Base


class LinkAddressesProtocolsCategoriesLabelsChains(Base):

    __tablename__ = 'l_addresses_protocols_categories_labels_chains'
    __table_args__ = {
        'comment': "Positions in protocol's contracts"
    }

    l_address_protocol_category_label_chain_id = Column(Integer, primary_key=True)
    l_address_label_chain_id = Column(Integer, ForeignKey('l_addresses_labels_chains.l_address_label_chain_id'), nullable=False)
    l_address_protocol_category_chain_id = Column(Integer, ForeignKey('l_addresses_protocols_categories_chains.l_address_protocol_category_chain_id'), nullable=False)
