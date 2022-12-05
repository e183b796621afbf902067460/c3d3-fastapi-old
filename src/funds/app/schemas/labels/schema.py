from pydantic import BaseModel, Field


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayloadSchema(BaseModel):
    sub: int = None
    exp: int = None


class LabelSignUpSchema(BaseModel):
    username: str = Field(..., min_length=6, max_length=24)
    password: str = Field(..., min_length=6, max_length=24)


class LabelORMSchema(BaseModel):
    h_label_id: int
    h_label_name: str

    class Config:
        orm_mode = True

