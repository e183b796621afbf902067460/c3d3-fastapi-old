from sqlalchemy import Column, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr
from fastapi_utils.camelcase import camel2snake

from app.orm.base.main import Base


class lProtocolsSpecifications(Base):

    @declared_attr
    def __tablename__(cls) -> str:
        return camel2snake(cls.__name__)

    l_protocol_specification_id = Column(Integer, primary_key=True)

    h_protocol_id = Column(Integer, ForeignKey('h_protocols.h_protocol_id'), nullable=False)
    h_specification_id = Column(Integer, ForeignKey('h_specifications.h_specification_id'), nullable=False)
    l_protocol_specification_load_ts = Column(DateTime, server_default=func.now(), nullable=False)
