from pydantic import BaseModel

class TrackSchema(BaseModel):
    id_album: int
    title: str
    duration: int