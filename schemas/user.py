from pydantic import BaseModel

class UserSchema(BaseModel):
    user_name: str
    email: str
    senha: str    