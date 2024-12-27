from sqlalchemy.orm import Session

from app import models,schemas


# 通过 user_id 来查询 user
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.u_id == user_id).first()

# 通过 account 来查询 user
def get_user_by_account(db: Session, account: str):
    return db.query(models.User).filter(models.User.account == account).first()

# 创建用户 （提供 account 和 password）
def create_user(db: Session, user:schemas.UserCreate):
    db_user = models.User(account = user.account,
                          password = user.password,
                          coin = 100)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_details(db: Session, account: str):
    user = get_user_by_account(db, account=account)
    if not user:
        return None
    return {"like": user.like, "coin": user.coin}