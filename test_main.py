from fastapi.testclient import TestClient
from app.database import DB_URL
from app.models import Base, User
from main import app
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

client = TestClient(app)

# 这里使用 SQLite 内存数据库作为示例，生产环境中可以使用 MySQL/PostgreSQL 等

# 创建数据库引擎
engine = create_engine(DB_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Pytest fixture: 初始化数据库并清空数据
@pytest.fixture(scope="module")
def reset_db():
    # 创建所有表（如果表未创建）
    Base.metadata.create_all(bind=engine)

    # 获取数据库会话
    db = SessionLocal()

    # 在测试前清空表中的所有内容
    db.query(User).delete()  # 假设你有一个 User 表
    db.commit()

    # Yield 控制权给测试函数
    yield db

    db.close()

    db.query(User).delete()
    db.commit()
    Base.metadata.drop_all(bind=engine)  # 测试结束后重置并清空数据库


def test_post_user(reset_db):
    response = client.post(
        "/users/signup",
        json={"account": "user1", "password": "password1"}
    )
    assert response.status_code == 200


def test_get_user_fail(reset_db):
    response = client.post(
        "/users/login",
        data={"username": "user1", "password": "wrong_password1"}
    )
    assert response.status_code == 401
    print(response.json())


def test_get_user_success(reset_db):
    response = client.post(
        "/users/login",
        data={"username": "user1", "password": "password1"}
    )
    assert response.status_code == 200
    print(response.json())
