from pydantic import BaseModel

class ComentSchema(BaseModel):
    id_user: int
    id_review: int
    content: str
    date_time: str