from fastapi import Form
from pydantic import BaseModel

class UserSchema(BaseModel):
    user_name: str
    email: str
    senha: str

    @classmethod
    def as_form(cls, user_name: str = Form(...), email: str = Form(...), senha: str = Form(...)):
        return cls(user_name=user_name, email=email, senha=senha) 