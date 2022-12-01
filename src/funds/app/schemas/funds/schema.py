from pydantic import BaseModel


class FundSchema(BaseModel):
    username: str


class FundCreateSchema(FundSchema):
    password: str


class FundORMSerializeSchema(BaseModel):
    h_label_id: int
    h_label_name: str


class FundORMDeserializeSchema(FundORMSerializeSchema):
    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'
