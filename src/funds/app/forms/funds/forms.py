from pydantic import BaseModel


class LabelForm(BaseModel):
    name: str
    password: str

