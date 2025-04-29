"""
檔案：user.py
用途：用戶資料庫操作
功能：
- 提供用戶相關的 CRUD 操作
- 處理用戶資料的查詢和更新
"""

from sqlalchemy.orm import Session
from ..models.user import User
from ..schemas.user import UserCreate, UserUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    """
    根據 ID 獲取用戶
    
    Args:
        db: 資料庫會話
        user_id: 用戶 ID
    
    Returns:
        User: 用戶物件
    """
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """
    根據電子郵件獲取用戶
    
    Args:
        db: 資料庫會話
        email: 電子郵件
    
    Returns:
        User: 用戶物件
    """
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    獲取用戶列表
    
    Args:
        db: 資料庫會話
        skip: 跳過的記錄數
        limit: 返回的最大記錄數
    
    Returns:
        List[User]: 用戶列表
    """
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: UserCreate):
    """
    創建新用戶
    
    Args:
        db: 資料庫會話
        user: 用戶創建資料
    
    Returns:
        User: 新創建的用戶物件
    """
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        email=user.email,
        password_hash=hashed_password,
        username=user.username,
        name=user.name,
        gender=user.gender,
        age=user.age,
        height=user.height,
        weight=user.weight,
        goal=user.goal,
        calorie_goal=user.calorie_goal,
        protein_goal=user.protein_goal,
        carbs_goal=user.carbs_goal,
        fat_goal=user.fat_goal
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate):
    """
    更新用戶資料
    
    Args:
        db: 資料庫會話
        user_id: 用戶 ID
        user: 用戶更新資料
    
    Returns:
        User: 更新後的用戶物件
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        update_data = user.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    """
    刪除用戶
    
    Args:
        db: 資料庫會話
        user_id: 用戶 ID
    
    Returns:
        bool: 是否成功刪除
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False 