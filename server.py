from fastapi import Depends, FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import (get_db, Session)

from models import Filme
from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse

from schemas.filme import FilmeSchema

from typing import List

app = FastAPI()

origins = ['*', 'http://localhost:8000']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def show_devices():
    return {"SUCCESS"}


@app.post("/add_filme")
def add_filme(filme_schema: FilmeSchema, db: Session=Depends(get_db)):
    #data = FilmeSchema(titulo='ta dando onda', capa='C:\\Users\\davig\\Documents\\projeto_eng_software\\ta_dando_onda.jpg')
    data = Filme(**filme_schema.dict())
    db.add(data)
    db.commit()
    return ("OK")


@app.get("/filmes")
def get_filmes(db: Session=Depends(get_db)):
    banco_dados: List[Filme] = db.query(Filme).all()
    return banco_dados