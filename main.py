import csv
import json
import logging

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



def update_hot_videos_once(db: Session):
    with open("test.json", mode='r', encoding='utf-8') as infile:
        data = json.load(infile)
    for item in data:
        video_info = item['name']
        video_url = item['url']
        cover_url = item['cover_url']
        like = item['like']
        coin = item['coin']
        type=item['type']
        video_schema = schemas.VideoCreate(url=video_url, name=video_info, cover_url=cover_url, like=like, coin=coin,type=type)
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
# 发送我的界面中的数据
@app.post("/user/detail", response_model=schemas.UserDetailResponse)
async def get_user_detail(user_detail_request: schemas.UserDetailRequest, db: Session = Depends(get_db)):
    user_details = crud.get_user_details(db, account=user_detail_request.account)
    if not user_details:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 获取用户的 like 字段
    likes = user_details["like"].split('|')
    
    # 定义类别和对应的索引
    categories = ["鬼畜类", "美食类", "生活类", "游戏类"]
    
    # 计算总喜好值
    total_likes = sum(map(int, likes))
    
    # 计算每个类别的百分比
    percentages = [f"{category}:{int(like) / total_likes * 100:.2f}%" for category, like in zip(categories, likes)]
    
    # 生成返回字符串
    result = ";".join(percentages)
    
    return {"like": result, "coin": user_details["coin"]}


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


# 获取首页视频
@app.post("/video/homepage", response_model=List[VideoResponse])
def get_homepage_videos(account: schemas.UserDetailRequest, db: Session = Depends(get_db)):
    homepage_videos = crud.get_homepage_videos_by_like(db, account=account.account, num=8)
    if not homepage_videos:
        raise HTTPException(status_code=404, detail="Video not found")
    return homepage_videos


@app.post("/video/cate", response_model=List[VideoResponse])
def get_cate_videos(video: schemas.VideoType, db: Session = Depends(get_db)):
    # print(json.loads(video.type)["kind"])
    cate_videos = crud.get_videos_by_type(db, json.loads(video.type)["kind"])
    if not cate_videos:
        raise HTTPException(status_code=404, detail="Video not found")
    return cate_videos
    # return []

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
    print(name.name)
    name_videos = crud.get_videos_by_name(db, name.name)
    if not name_videos:
        raise HTTPException(status_code=404, detail="Video not found")
    return name_videos

# 更新用户的硬币数和视频的硬币数
@app.post("/video/getcoin", response_model=schemas.UpdateCoinResponse)
def update_coin_and_like(update_coin_request: schemas.UpdateCoinRequest, db: Session = Depends(get_db)):
    result = crud.update_coin_and_like(db, account=update_coin_request.account, bv=update_coin_request.bv)
    if not result:
        raise HTTPException(status_code=404, detail="User or Video not found")
    user_pydantic = schemas.User.from_orm(result["user"])
    video_pydantic = schemas.VideoResponse.from_orm(result["video"])
    return schemas.UpdateCoinResponse(
        message="Update successful",
        user=user_pydantic,
        video=video_pydantic
    )

# 更新视频的点赞数
@app.post("/video/getlike", response_model=VideoResponse)
def update_video_like(video: schemas.VideoBv, db: Session = Depends(get_db)):
    updated_video = crud.increment_video_like(db, bv=video.bv)
    if not updated_video:
        raise HTTPException(status_code=404, detail="Video not found")
    return updated_video

def init_config():
    with SessionLocal() as db:
        config = db.query(models.Config).first()
        if not config:  # 如果没有配置记录，则插入默认配置
            new_config = models.Config(test_json_loaded=False)  # 初始时未加载
            db.add(new_config)
            db.commit()
            db.refresh(new_config)


@app.on_event("startup")
async def startup_event():
    init_config()
    logger = logging.getLogger("uvicorn.access")
    handler = logging.handlers.RotatingFileHandler("api.log", mode="a", maxBytes=100 * 1024, backupCount=3)
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

    with SessionLocal() as db:
        config = db.query(models.Config).first()  # 获取配置表的第一条记录
        if config and not config.test_json_loaded:
            print("##############################################################################")
            is_to_execute = str(input(
                "请您打开设置的数据库,运行下面指令:\n`alter table users convert to character set  utf8mb4`\n和`alter table video convert to character set  utf8mb4`,\n在运行完成以后,请输入y进行测试数据导入(y/n)"))
            if is_to_execute != "y":
                exit()
            # 如果未加载过test_json文件，执行加载操作
            update_hot_videos_once(db)  # 加载test_json文件
            config.test_json_loaded = True
            db.commit()  # 提交更新
            print("加载成功")