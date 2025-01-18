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
    cover_url: str


class VideoCreate(VideoBase):
    like: int
    coin: int
    type: int


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
    type: str


class VideoLike(BaseModel):
    like: int


class VideoCoin(BaseModel):
    coin: int


class VideoName(BaseModel):
    name: str


class UpdateCoinRequest(BaseModel):
    account: str
    bv: int

class UpdateCoinResponse(BaseModel):
    message: str
    user: User
    video: VideoResponse