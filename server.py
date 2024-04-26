from fastapi import Depends, FastAPI, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import (get_db, Session)

from sqlalchemy.orm import Session
from fastapi import status
from fastapi.responses import JSONResponse

from models.models import User, Album, Review, Followers
from schemas.user import UserSchema
from schemas.album import AlbumSchema
from schemas.review import ReviewSchema
from schemas.follower import FollowerSchema

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


@app.get("/user")
def get_filmes(db: Session=Depends(get_db)):
    data: List[User] = db.query(User).all()
    return data


@app.get("/search_user/{user_name}")
def get_filmes(user_name: str, db: Session=Depends(get_db)):
    data: List[User] = db.query(User).filter(User.user_name == user_name).all()
    return data


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


@app.get("/album")
def get_albuns(db: Session=Depends(get_db)):
    data: List[Album] = db.query(Album).all()
    return data


@app.post("/add_album")
def add_album(album_schema: AlbumSchema, db: Session=Depends(get_db)):
    data = Album(**album_schema.dict())
    db.add(data)
    db.commit()
    return ("OK")


@app.get("/review/{review_id}")
def get_review(review_id: int, db: Session=Depends(get_db)):
    data: List[Review] = db.query(Review).filter(Review.id == review_id).all()
    if not data:
        return "not found"
    return data


@app.post("/add_review")
def add_review(review_schema: ReviewSchema, db: Session=Depends(get_db)):
    data = Review(**review_schema.dict())
    db.add(data)
    db.commit()
    return ("OK")


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


@app.post("/add_follower")
def add_follower(follower_schema: FollowerSchema, db: Session=Depends(get_db)):
    data = Followers(**follower_schema.dict())
    db.add(data)
    db.commit()
    return ("OK")