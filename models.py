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

Base.metadata.create_all(bind=engine)