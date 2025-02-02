import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from passlib.hash import bcrypt

from app import models, schemas
from app import crud, security
from app.database import SessionLocal, engine
from app.security import Token

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#Dependency
def get_db():
    db = SessionLocal()
    try :
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
def login_user(db: Session, form_data: OAuth2PasswordRequestForm):
    user = verify_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(hours=1)
    access_token = create_access_token(data={"sub": user.account}, expires_delta=access_token_expires)
    return {"account": user.account, "access_token": access_token, "token_type": "bearer"}



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
@app.post("/users/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login_user(db, form_data)


# 发送我的界面中的数据
@app.post("/user/detail")
async def get_user_detail(user_detail_request: schemas.UserDetailRequest, db: Session = Depends(get_db)):
    user_details = crud.get_user_details(db, account=user_detail_request.account)
    if not user_details:
        raise HTTPException(status_code=404, detail="User not found")
    return schemas.UserDetailResponse(**user_details)