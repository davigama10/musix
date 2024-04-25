from pydantic import BaseModel

class AlbumSchema(BaseModel):
    title: str
    year: int
    author: str
    gender: str
    infos: str