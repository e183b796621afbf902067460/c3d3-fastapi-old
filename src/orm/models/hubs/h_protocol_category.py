from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func

from src.orm.base.main import Base


class HubProtocolsCategories(Base):

    __tablename__ = 'h_protocols_categories'

    h_protocol_category_id = Column(Integer, primary_key=True)
    h_protocol_category_name = Column(Text, nullable=False)
    h_network_load_ts = Column(DateTime, server_default=func.now(), nullable=False)
