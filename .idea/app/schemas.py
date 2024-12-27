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