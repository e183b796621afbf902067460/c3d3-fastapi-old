from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func

from src.orm.base.main import Base


class HubProtocols(Base):

    __tablename__ = 'h_protocols'

    h_protocol_id = Column(Integer, primary_key=True)  # PK
    h_protocol_name = Column(Text, nullable=False)
    h_protocol_load_ts = Column(DateTime, server_default=func.now(), nullable=False)
