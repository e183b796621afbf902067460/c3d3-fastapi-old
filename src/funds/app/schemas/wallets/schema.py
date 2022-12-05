from pydantic import BaseModel


class WalletORMSchema(BaseModel):
    h_address: str
    h_network_name: str
    h_network_endpoint: str

    class Config:
        orm_mode = True
