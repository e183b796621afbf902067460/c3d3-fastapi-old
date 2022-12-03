from pydantic import BaseModel


class LabelSchema(BaseModel):
    username: str


class LabelCreateSchema(LabelSchema):
    password: str


class LabelORMSerializeSchema(BaseModel):
    h_label_id: int
    h_label_name: str


class LabelORMDeserializeSchema(LabelORMSerializeSchema):
    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'
