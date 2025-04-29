"""
檔案：user.py
用途：用戶模型
功能：
- 定義用戶資料表結構
- 提供用戶相關的資料庫操作
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from ..config.database import Base

class User(Base):
    """
    用戶模型
    
    屬性：
    - id: 用戶 ID
    - username: 用戶名稱
    - email: 電子郵件
    - password_hash: 密碼雜湊
    - name: 姓名
    - gender: 性別
    - age: 年齡
    - height: 身高 (cm)
    - weight: 體重 (kg)
    - goal: 目標
    - calorie_goal: 每日熱量目標
    - protein_goal: 每日蛋白質目標
    - carbs_goal: 每日碳水化合物目標
    - fat_goal: 每日脂肪目標
    - is_active: 是否啟用
    - created_at: 建立時間
    - updated_at: 更新時間
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)
    height = Column(Float)
    weight = Column(Float)
    goal = Column(String)
    calorie_goal = Column(Float)
    protein_goal = Column(Float)
    carbs_goal = Column(Float)
    fat_goal = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 