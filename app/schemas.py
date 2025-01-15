from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    account: str
    password: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    u_id: int
    like: Optional[str] = ""
    coin: int = 100  # 为 coin 字段设置默认值 100

class UserDetailRequest(BaseModel):
    account: str

class UserDetailResponse(BaseModel):
    like: Optional[str] = ""  # 为 like 字段设置默认值 ""
    coin: int

class VideoBase(BaseModel):
    url: str
    name: str

class VideoCreate(VideoBase):
    pass

class Video(VideoBase):
    like : int = 0
    coin : int = 0
    type : int = 1

class VideoBv(BaseModel):
    bv : int