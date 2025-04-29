from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """用戶基礎模型"""
    email: EmailStr
    name: str

class UserCreate(UserBase):
    """創建用戶模型"""
    password: str = Field(..., min_length=8)

class UserUpdate(BaseModel):
    """更新用戶模型"""
    name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)

class UserInDB(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class User(UserInDB):
    pass 