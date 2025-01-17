import csv
import json

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from passlib.hash import bcrypt

from typing import List
from app import models, schemas
from app import crud, security
from app.database import SessionLocal, engine
from app.schemas import VideoResponse
from app.security import Token
import requests
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# 验证用户
def verify_user(db: Session, username: str, password: str):
    user = crud.get_user_by_account(db, account=username)
    if not user or not pwd_context.verify(password, user.password):
        return False
    return user


# 生成令牌
def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    expires = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expires})
    encoded_jwt = jwt.encode(to_encode, security.SECURITY_KEY, algorithm=security.ALGORITHMS)
    return encoded_jwt


# 登录逻辑
def login_user(db: Session, form_data: schemas.UserBase):
    user = verify_user(db, form_data.account, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password",
                            headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(hours=1)
    access_token = create_access_token(data={"sub": user.account}, expires_delta=access_token_expires)
    return {"account": user.account, "access_token": access_token, "token_type": "bearer"}


def csv_to_json(csv_file, json_file):
    # 打开 CSV 文件并读取数据
    with open(csv_file, mode='r', encoding='utf-8') as infile:
        # 使用 csv.DictReader 自动将 CSV 的每一行解析为字典
        reader = csv.DictReader(infile)

        # 将 CSV 数据转存到列表中
        data = []
        for row in reader:
            data.append(row)

    # 将数据写入 JSON 文件
    with open(json_file, mode='w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)


def update_hot_videos_once(db: Session):
    csv_to_json("B站TOP100.csv", "myjson")
    with open("myjson", mode='r', encoding='utf-8') as infile:
        data = json.load(infile)
    for item in data:
        video_info = item['视频标题']
        video_url = item['视频地址']
        cover_url = item['封面地址']
        video_schema = schemas.VideoCreate(url=video_url, name=video_info, cover_url=cover_url)
        crud.create_video(db, video_schema)
# 用户注册功能
@app.post('/users/signup', response_model=schemas.User)
def post_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_account(db, account=user.account)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    return crud.create_user(db=db, user=user)


# 用户登录功能
# 用户登录功能
@app.post("/users/login")
async def login(form_data: schemas.UserBase, db: Session = Depends(get_db)):
    return login_user(db, form_data)

# 登录逻辑



# 发送我的界面中的数据
@app.post("/user/detail")
async def get_user_detail(user_detail_request: schemas.UserDetailRequest, db: Session = Depends(get_db)):
    user_details = crud.get_user_details(db, account=user_detail_request.account)
    if not user_details:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserDetailResponse(**user_details)


@app.post("/video/bv",response_model=VideoResponse)
async def get_video_by_bv(video: schemas.VideoBv, db: Session = Depends(get_db)):
    target_video = crud.get_video_by_bv(db, bv=video.bv)
    if not target_video:
        raise HTTPException(status_code=404, detail="Video not found")
    return target_video


@app.post("/video/hot", response_model=List[VideoResponse])
def get_hot_videos(db: Session = Depends(get_db)):
    # 查询点赞数最多的10个视频
    hot_videos = crud.get_hot_videos(db)
    if not hot_videos:
        raise HTTPException(status_code=404, detail="Video not found")
    return hot_videos


@app.post("/video/homepage", response_model=List[VideoResponse])
def get_homepage_videos(account:schemas.UserDetailRequest,db: Session = Depends(get_db)):
    homepage_videos = crud.get_random_videos_by_num(db, num=8)
    if not homepage_videos:
        raise HTTPException(status_code=404, detail="Video not found")
    return homepage_videos


@app.post("/video/cate", response_model=List[VideoResponse])
def get_cate_videos(video: schemas.VideoType, db: Session = Depends(get_db)):
    cate_videos = crud.get_videos_by_type(db, video.type)
    if not cate_videos:
        raise HTTPException(status_code=404, detail="Video not found")
    return cate_videos

@app.post("/video/like",response_model=schemas.VideoLike)
def get_like_videos(video: schemas.VideoBv, db: Session = Depends(get_db)):
    like = crud.get_like_by_bv(db, video.bv)
    if not like:
        raise HTTPException(status_code=404, detail="Video not found")
    return like

@app.post("/video/coin",response_model=schemas.VideoCoin)
def get_coin_videos(video: schemas.VideoBv, db: Session = Depends(get_db)):
    coin = crud.get_coin_by_bv(db, video.bv)
    if not coin:
        raise HTTPException(status_code=404, detail="Video not found")
    return coin

@app.post("/video/name", response_model=List[VideoResponse])
def get_name_videos(name: schemas.VideoName, db: Session = Depends(get_db)):
    name_videos = crud.get_videos_by_name(db, name.name)
    if not name_videos:
        raise HTTPException(status_code=404, detail="Video not found")
    return name_videos

@app.on_event("startup")
async def startup_event():
    with SessionLocal() as db:
        update_hot_videos_once(db)