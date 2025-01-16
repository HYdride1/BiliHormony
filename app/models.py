from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    u_id = Column(Integer, primary_key=True, index=True, nullable=False)
    account = Column(String(255), index=True, unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    like = Column(String(255))
    coin = Column(Integer, nullable=False)

class Video(Base):
    __tablename__ = "video"
    bv = Column(Integer, primary_key=True, index=True, nullable= False)
    name = Column(String(255),index=True, nullable=False)
    type = Column(Integer, nullable=False)
    like = Column(Integer, nullable=False, default=0)
    coin = Column(Integer, nullable=False,default= 0 )
    url = Column(String(255), nullable=False)