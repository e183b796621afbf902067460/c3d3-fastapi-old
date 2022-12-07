from sqlalchemy import Column, Integer, ForeignKey

from src.orm.base.main import Base


class LinkProtocolsCategories(Base):

    __tablename__ = 'l_protocols_categories'
    __table_args__ = {
        'comment': "Protocol's Categories"
    }

    l_protocol_category_id = Column(Integer, primary_key=True)  # PK
    h_protocol_id = Column(Integer, ForeignKey('h_protocols.h_protocol_id'), nullable=False)
    h_protocol_category_id = Column(Integer, ForeignKey('h_protocols_categories.h_protocol_category_id'), nullable=False)
