from fastapi import Form
from pydantic import BaseModel

class UserLoginSchema(BaseModel):
    username: str
    senha: str

    @classmethod
    def as_form(cls, username: str = Form(...), senha: str = Form(...)):
        return cls(username=username, senha=senha) 