from pydantic import BaseModel
from datetime import datetime


class NewChainSchema(BaseModel):
    network_name: str
    native_chain_token: str
    rpc_node: str
    block_limit: int
    network_uri: str
    network_api_key: str


class NewBidsAndAsksSchema(BaseModel):
    pool_address: str
    network_name: str
    protocol_name: str
    specification_name: str
    is_reverse: bool


class NewHedgeToBorrowsSchema(BaseModel):
    wallet_address: str
    token_address: str
    network_name: str
    label_name: str
    protocol_name: str
    specification_name: str


class NewHedgeToSuppliesSchema(NewHedgeToBorrowsSchema): ...


class NewWalletBalancesSchema(BaseModel):
    wallet_address: str
    token_address: str
    network_name: str
    label_name: str


class ChainORMSchema(BaseModel):
    h_chain_id: int

    h_network_name: str
    h_native_chain_token: str
    h_network_rpc_node: str
    h_network_block_limit: int
    h_network_uri: str
    h_network_api_key: str

    h_network_load_ts: datetime

    class Config:
        orm_mode = True


class AddressChainProtocolSpecificationORMSchema(BaseModel):
    l_address_chain_protocol_specification_id: int
    l_address_chain_id: int
    l_protocol_specification_id: int
    l_address_chain_protocol_specification_load_ts: datetime

    class Config:
        orm_mode = True


class AddressChainProtocolSpecificationLabelORMSchema(BaseModel):
    l_address_chain_protocol_specification_label_id: int
    l_address_chain_label_id: int
    l_address_chain_protocol_specification_id: int
    l_address_chain_protocol_specification_label_load_ts: datetime

    class Config:
        orm_mode = True


class TokenOnWalletORMSchema(BaseModel):
    l_token_on_wallet_id: int
    l_address_chain_id: int
    l_address_chain_label_id: int
    l_token_on_wallet_load_ts: datetime

    class Config:
        orm_mode = True
