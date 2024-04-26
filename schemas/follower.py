from pydantic import BaseModel

class FollowerSchema(BaseModel):
    id_user: int
    id_follower: int