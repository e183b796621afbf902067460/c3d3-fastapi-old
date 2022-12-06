from sqlalchemy import Column, Integer, Text, DateTime
from sqlalchemy.sql import func

from src.orm.base.main import Base


class HubLabels(Base):

    __tablename__ = 'h_labels'

    h_label_id = Column(Integer, primary_key=True)  # PK
    h_label_name = Column(Text, unique=True, nullable=False)
    h_label_password = Column(Text, nullable=False)
    h_label_load_ts = Column(DateTime, server_default=func.now(), nullable=False)
