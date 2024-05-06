from pydantic import BaseModel
from fastapi import Form

class ReviewUserSchema(BaseModel):
    review_content: str
    rate: int

    @classmethod
    def as_form(cls,
                review_content: str = Form(...), 
                rate: int = Form(...),):
        return cls(review_content=review_content, rate=rate) 