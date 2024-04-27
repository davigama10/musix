from pydantic import BaseModel
from typing import Optional, Union
from database import Base, engine
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, nullable=False)
    bio = Column(String, nullable=True)
    email = Column(String, nullable=False)
    senha = Column(String, nullable=False)
    followers = Column(Integer, nullable=True)
    following = Column(Integer, nullable=True)
    reviews = Column(Integer, nullable=True)


class Followers(Base):
    __tablename__ = "followers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    id_follower = Column(Integer, ForeignKey('users.id'), nullable=False)

class Review(Base):
    __tablename__ = "review"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    id_album = Column(Integer, ForeignKey('album.id'), nullable=False)
    review_content = Column(String, nullable=True)
    date_time = Column(String, nullable=True)
    rate = Column(Integer, nullable=False)
    likes = Column(Integer, nullable=True)
    coments = Column(Integer, nullable=True)


class Album(Base):
    __tablename__ = "album"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    author = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    infos = Column(String, nullable=False)
    average_rating = Column(Float, nullable=True)
    reviews_number = Column(Integer, nullable=True)
    in_lists = Column(Integer, nullable=True)
    tracks = Column(Integer, nullable=True)


class Coment(Base):
    __tablename__ = "coment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    id_review = Column(Integer, ForeignKey('review.id'), nullable=False)
    content = Column(String, nullable=False)
    date_time = Column(String, nullable=True)
    likes = Column(Integer, nullable=True)


class List(Base):
    __tablename__ = "list"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    date_time = Column(String, nullable=True)
    content_amount = Column(Integer, nullable=False)


class Track(Base):
    __tablename__ = "track"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_album = Column(Integer, ForeignKey('album.id'), nullable=False)
    title = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)


Base.metadata.create_all(bind=engine)