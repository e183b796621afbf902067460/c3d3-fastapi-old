from pydantic import BaseModel


class SessionORMSchema(BaseModel):
    h_session_id: int
    h_session_name: str

    class Config:
        orm_mode = True


class SessionLoginSchema(BaseModel):
    username: str
    password: str
