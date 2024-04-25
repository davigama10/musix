from pydantic import BaseModel

class UserSchema(BaseModel):
    user_name = str
    email = str
    senha = str
    bio = str
    follower = int
    following = int
    reviews = int