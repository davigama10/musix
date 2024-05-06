from pydantic import BaseModel
from fastapi import Form

class ReviewSchema(BaseModel):
    id_user: int
    id_album: int
    review_content: str
    date_time: str
    rate: int