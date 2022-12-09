from pydantic import BaseModel


class PoolORMSchema(BaseModel):
    l_address_chain_name: str
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
    pool_name: str


class PoolDeleteSchema(PoolAddSchema):
    pass
