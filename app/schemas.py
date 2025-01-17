import random
from typing import Optional
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    account: str
    password: str

class UserCreate(UserBase):
    coin: int = 100  # 为 coin 字段设置默认值 100
    like: int = Field(default_factory=lambda: random.choice([1, 2, 3, 4]), ge=1, le=4)  # 随机选择 1, 2, 3, 4 中的一个

class User(UserBase):
    u_id: int
    like: Optional[int] = Field(None, ge=1, le=4)  # 限制 like 为 1, 2, 3, 4 中的一个
    coin: int

class UserDetailRequest(BaseModel):
    account: str

class UserDetailResponse(BaseModel):
    like: Optional[int] = Field(None, ge=1, le=4)  # 限制 like 为 1, 2, 3, 4 中的一个
    coin: int


class VideoBase(BaseModel):
    url: str
    name: str
    cover_url: str


class VideoCreate(VideoBase):
    like: int
    coin: int


class Video(VideoBase):
    like: int = 0
    coin: int = 0
    type: int = 1


class VideoBv(BaseModel):
    bv: int


class VideoResponse(BaseModel):
    bv: int
    type: int
    name: str
    like: int
    coin: int
    url: str
    cover_url: str


class VideoType(BaseModel):
    type: int


class VideoLike(BaseModel):
    like: int


class VideoCoin(BaseModel):
    coin: int


class VideoName(BaseModel):
    name: str
