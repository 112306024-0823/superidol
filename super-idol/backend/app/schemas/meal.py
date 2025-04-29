"""餐點模式"""
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime

class MealBase(BaseModel):
    """餐點基礎模式"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    calories: float = Field(..., ge=0)
    protein: float = Field(..., ge=0)
    carbs: float = Field(..., ge=0)
    fat: float = Field(..., ge=0)

class MealCreate(MealBase):
    """創建餐點模式"""
    pass

class MealUpdate(BaseModel):
    """更新餐點模式"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    calories: Optional[float] = Field(None, ge=0)
    protein: Optional[float] = Field(None, ge=0)
    carbs: Optional[float] = Field(None, ge=0)
    fat: Optional[float] = Field(None, ge=0)

class MealInDB(MealBase):
    """數據庫中的餐點模式"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Meal(MealInDB):
    """餐點響應模式"""
    pass 