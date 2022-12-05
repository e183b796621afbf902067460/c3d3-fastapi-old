from pydantic import BaseModel, Field
from uuid import UUID


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayloadSchema(BaseModel):
    sub: UUID = None
    exp: int = None


class LabelSignUpSchema(BaseModel):
    username: str = Field(..., min_length=6, max_length=24)
    password: str = Field(..., min_length=6, max_length=24)


class LabelORMlSchema(BaseModel):
    h_label_id: int
    h_label_name: str

    class Config:
        orm_mode = True

