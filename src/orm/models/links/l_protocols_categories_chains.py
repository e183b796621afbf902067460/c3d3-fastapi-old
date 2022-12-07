from sqlalchemy import Column, Integer, ForeignKey

from src.orm.base.main import Base


class LinkProtocolsCategoriesChains(Base):

    __tablename__ = 'l_protocols_categories_chains'
    __table_args__ = {
        'comment': "Chain's Protocols Categories"
    }

    l_protocol_category_chain_id = Column(Integer, primary_key=True)
    l_protocol_category_id = Column(Integer, ForeignKey('l_protocols_categories.l_protocol_category_id'), nullable=False)
    h_chain_id = Column(Integer, ForeignKey('h_chains.h_chain_id'), nullable=False)
