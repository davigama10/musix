from pydantic import BaseModel
from typing import Optional, Union
from database import Base, engine
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Boolean, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

class Filme(Base):
    __tablename__ = "filme"
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String, nullable=False)
    capa = Column(String, nullable=False)


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


class Review(Base):
    __tablename__ = "review"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    id_album = Column(Integer, ForeignKey('album.id'), nullable=False)
    review_content = Column(String, nullable=False)
    date_time = Column(String, nullable=False)
    rate = Column(Integer, nullable=False)
    likes = Column(Integer, nullable=False)
    coments = Column(Integer, nullable=False)


class Album(Base):
    __tablename__ = "album"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    author = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    infos = Column(String, nullable=False)
    average_rating = Column(Float, nullable=False)
    reviews_number = Column(Integer, nullable=False)
    in_lists = Column(Integer, nullable=False)
    #tracks


class Coment(Base):
    __tablename__ = "coment"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    id_review = Column(Integer, ForeignKey('review.id'), nullable=False)
    content = Column(String, nullable=False)
    date_time = Column(String, nullable=False)
    likes = Column(Integer, nullable=False)


class List(Base):
    __tablename__ = "list"
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_user = Column(Integer, ForeignKey('users.id'), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    date_time = Column(String, nullable=False)
    content_amount = Column(Integer, nullable=False)


# class tracks


Base.metadata.create_all(bind=engine)