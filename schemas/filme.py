from pydantic import BaseModel


class FilmeSchema(BaseModel):
    titulo: str
    capa: str