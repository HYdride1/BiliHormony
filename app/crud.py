from sqlalchemy.orm import Session
from sqlalchemy import desc, func, update
from app import models, schemas
import random

# 通过 user_id 来查询 user
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.u_id == user_id).first()

# 通过 account 来查询 user
def get_user_by_account(db: Session, account: str):
    return db.query(models.User).filter(models.User.account == account).first()

# 创建用户 （提供 account 和 password）
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(account=user.account,
                          password=user.password,
                          coin=100,
                          like="30|30|30|30")  # 使用固定的占比字符串
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_details(db: Session, account: str):
    user = get_user_by_account(db, account=account)
    if not user:
        return None
    return {"like": user.like, "coin": user.coin}

def create_video(db: Session, video: schemas.VideoCreate):
    db_video = models.Video(name=video.name,
                            url=video.url,
                            cover_url=video.cover_url,
                            like=video.like,
                            coin=video.coin,
                            type=video.type)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video

def get_video_by_bv(db: Session, bv: int):
    return db.query(models.Video).filter(models.Video.bv == bv).first()

def get_hot_videos(db: Session):
    return db.query(models.Video).order_by(desc(models.Video.like)).limit(10).all()

def get_random_videos_by_num(db: Session, num=8):
    return db.query(models.Video).order_by(func.random()).limit(num).all()

def get_videos_by_type(db: Session, type):
    return db.query(models.Video).filter(models.Video.type == type).all()

def get_like_by_bv(db: Session, bv: int):
    return db.query(models.Video.like).filter(models.Video.bv == bv).first()

def get_coin_by_bv(db: Session, bv: int):
    return db.query(models.Video.coin).filter(models.Video.bv == bv).first()

def get_videos_by_name(db: Session, name: str):
    return db.query(models.Video).filter(models.Video.name.like(f"%{name}%")).all()

def update_coin_and_like(db: Session, account: str, bv: int):
    user = get_user_by_account(db, account=account)
    video = get_video_by_bv(db, bv=bv)
    
    if not user or not video:
        return None

    # 更新用户的 coin 数量
    user.coin -= 1

    # 更新用户的 like 值
    likes = user.like.split('|')
    likes[video.type - 1] = str(int(likes[video.type - 1]) + 1)
    user.like = '|'.join(likes)

    # 更新视频的 coin 数量
    video.coin += 1

    db.commit()
    return {"user": user, "video": video}

def increment_video_like(db: Session, bv: int):
    video = get_video_by_bv(db, bv=bv)
    if not video:
        return None

    # 更新视频的 like 数量
    video.like += 1
    db.commit()
    return video

def get_homepage_videos_by_like(db: Session, account: str, num=8):
    user = get_user_by_account(db, account=account)
    if not user:
        return None

    likes = user.like.split('|')
    total_likes = sum(map(int, likes))
    if total_likes == 0:
        return get_random_videos_by_num(db, num=num)

    # 计算每种类型的权重
    weights = [int(like) / total_likes for like in likes]

    # 获取所有视频
    videos = db.query(models.Video).all()

    # 按类型分组
    videos_by_type = {i: [] for i in range(1, len(likes) + 1)}
    for video in videos:
        videos_by_type[video.type].append(video)

    # 按权重随机抽取视频
    selected_videos = []
    for _ in range(num):
        type_index = random.choices(range(1, len(likes) + 1), weights=weights)[0]
        if videos_by_type[type_index]:
            selected_video = random.choice(videos_by_type[type_index])
            selected_videos.append(selected_video)
            videos_by_type[type_index].remove(selected_video)

    return selected_videos