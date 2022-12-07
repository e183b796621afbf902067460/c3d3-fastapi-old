from pydantic import BaseModel


class PoolORMSchema(BaseModel):
    h_address: str
    h_network_name: str
    h_network_endpoint: str
    h_protocol_name: str
    h_protocol_category_name: str

    class Config:
        orm_mode = True


class PoolAddSchema(BaseModel):
    address: str
    protocol: str
    protocol_category: str


class PoolDeleteSchema(PoolAddSchema):
    pass
