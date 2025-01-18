from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base
import random

# class User(Base):
#     __tablename__ = "users"
#     u_id = Column(Integer, primary_key=True, index=True, nullable=False)
#     account = Column(String(255), index=True, unique=True, nullable=False)
#     password = Column(String(255), nullable=False)
#     like = Column(String(255))
#     coin = Column(Integer, nullable=False)
    
# class RandomLikeDefault:
#     def __call__(self, context):
#         return str(random.choice(["鬼畜类", "生活类", "美食类", "游戏类"]))

# class User(Base):
#     __tablename__ = "users"
#     u_id = Column(Integer, primary_key=True, index=True, nullable=False)
#     account = Column(String(255), index=True, unique=True, nullable=False)
#     password = Column(String(255), nullable=False)
#     like = Column(String(255), default=RandomLikeDefault())  # 使用自定义的默认值生成器
#     coin = Column(Integer, nullable=False)

class FixedLikeDefault:
    def __call__(self, context):
        return "30|30|30|30"  # 返回固定格式的占比字符串

class User(Base):
    __tablename__ = "users"
    u_id = Column(Integer, primary_key=True, index=True, nullable=False)
    account = Column(String(255), index=True, unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    like = Column(String(255), default=FixedLikeDefault())  # 使用自定义的默认值生成器
    coin = Column(Integer, nullable=False)

class Video(Base):
    __tablename__ = "video"
    bv = Column(Integer, primary_key=True, index=True, nullable= False)
    name = Column(String(255),index=True, nullable=False)
    type = Column(Integer, nullable=False, default= 1 )
    like = Column(Integer, nullable=False, default= 0 )
    coin = Column(Integer, nullable=False,default= 0 )
    url = Column(String(255), nullable=False)
    cover_url = Column(String(255), nullable = False)


class Config(Base):
    __tablename__ = 'config'

    id = Column(Integer, primary_key=True, index=True)  # 配置表的唯一ID
    test_json_loaded = Column(Boolean, default=False)  # 用于标记是否加载过test_json文件