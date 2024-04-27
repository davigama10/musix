from pydantic import BaseModel

class ListSchema(BaseModel):
    id_user: int
    title: str
    description: str
