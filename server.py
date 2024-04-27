from fastapi import Depends, FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import (get_db, Session)

from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse

from models.models import User, Album, Review, Followers, Coment, Track, List
from schemas.user import UserSchema
from schemas.album import AlbumSchema
from schemas.review import ReviewSchema
from schemas.follower import FollowerSchema
from schemas.coment import ComentSchema
from schemas.track import TrackSchema
from schemas.list import ListSchema

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


#rota pra mostrar todos os usuários cadastrados
@app.get("/user")
def get_filmes(db: Session=Depends(get_db)):
    data: List[User] = db.query(User).all()
    return data


#rota para procurar um usuário pelo nome na url
@app.get("/search_user/{user_name}")
def get_filmes(user_name: str, db: Session=Depends(get_db)):
    data: List[User] = db.query(User).filter(User.user_name == user_name).all()
    return data


#rota para cadastrar um usuário
@app.post("/add_user")
def add_user(user_schema: UserSchema, db: Session=Depends(get_db)):
    data = User(**user_schema.dict())
    if not data.followers:
        data.followers = 0
    if not data.following:
        data.following = 0
    if not data.reviews:
        data.reviews = 0
    db.add(data)
    db.commit()
    return ("OK")


#rota para retornar todos os álbuns cadastrados
@app.get("/album")
def get_albuns(db: Session=Depends(get_db)):
    data: List[Album] = db.query(Album).all()
    return data


#rota para cadastrar um álbum
@app.post("/add_album")
def add_album(album_schema: AlbumSchema, db: Session=Depends(get_db)):
    data = Album(**album_schema.dict())
    data.reviews_number = 0
    data.average_rating = 0
    data.tracks = 0
    db.add(data)
    db.commit()
    return ("OK")


#rota para retornar uma review pelo id dela
@app.get("/review/{review_id}")
def get_review(review_id: int, db: Session=Depends(get_db)):
    data: List[Review] = db.query(Review).filter(Review.id == review_id).all()
    if not data:
        return "not found"
    return data


#rota para cadastrar uma review
@app.post("/add_review")
def add_review(review_schema: ReviewSchema, db: Session=Depends(get_db)):
    data = Review(**review_schema.dict())
    db.query(Album).filter(Album.id == data.id_album).update({"reviews_number": Album.reviews_number + 1})
    data.coments = 0
    data.likes = 0
    db.add(data)
    db.commit()
    return ("OK")


#rota para buscar os seguidores de um usuário pelo id dele
@app.get("/followers/{user_id}")
def get_followers(user_id: int, db: Session=Depends(get_db)):
    data: List[Followers] = db.query(Followers).filter(Followers.id_user == user_id).all()
    data1 = []
    if not data:
        return "not found"
    for a in data:
        x = db.query(User).filter(User.id == a.id_follower).all()
        data1.append(x)
    return data1


#rota para adicionar um seguidor para um usuário 
#+ incrementa o número de followers do usuário
#+ incrementa o número de following do follower
@app.post("/add_follower")
def add_follower(follower_schema: FollowerSchema, db: Session=Depends(get_db)):
    data = Followers(**follower_schema.dict())
    db.query(User).filter(User.id == data.id_user).update({"followers": User.followers + 1})
    db.query(User).filter(User.id == data.id_follower).update({"following": User.following + 1})
    db.add(data)
    db.commit()
    return ("OK")


#rota para retornar todos os comentários de uma review
@app.get("/coments/{review_id}")
def get_coments(review_id: int, db: Session=Depends(get_db)):
    data: List[Coment] = db.query(Coment).filter(Coment.id_review == review_id).all()    
    return data

#rota para cadastrar um comentário
#+ incrementa o número de comentarios da review
@app.post("/add_coment")
def add_coment(coment_schema: ComentSchema, db: Session=Depends(get_db)):
    data = Coment(**coment_schema.dict())
    db.query(Review).filter(Review.id == data.id_review).update({"coments": Review.coments + 1})
    data.likes = 0
    db.add(data)
    db.commit()
    return ("OK")


#rota para retornar todas as tracks de um album
@app.get("/tracks/{album_id}")
def get_tracks(album_id: int, db: Session=Depends(get_db)):
    data: List[Track] = db.query(Track).filter(Track.id_album == album_id).all()    
    return data


#rota para cadastrar musicas em um album
#tem que passar uma lista no json dessa rota
@app.post("/add_tracks")
def add_tracks(track_schema: List[TrackSchema], db: Session=Depends(get_db)):
    data = [Track(**track.dict()) for track in track_schema]
    db.query(Album).filter(Album.id == data[0].id_album).update({"tracks": Album.tracks + 1})
    db.add_all(data)
    db.commit()
    return ("OK")


#rota para adicionar uma lista de musicas
# @app.post("/add_list")
# def add_list(list_schema: ListSchema, db: Session=Depends(get_db)):
#     data = List(**list_schema.dict())
#     db.query(Review).filter(Review.id == data.id_review).update({"coments": Review.coments + 1})
#     if not data.description:
#         data.description = " "
#     db.add(data)
#     db.commit()
#     return ("OK")