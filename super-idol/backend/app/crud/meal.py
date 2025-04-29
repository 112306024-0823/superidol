"""餐點CRUD操作"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.meal import Meal
from app.schemas.meal import MealCreate, MealUpdate

def get_meal(db: Session, meal_id: int) -> Optional[Meal]:
    """獲取單個餐點"""
    return db.query(Meal).filter(Meal.id == meal_id).first()

def get_meals(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None
) -> List[Meal]:
    """獲取餐點列表"""
    query = db.query(Meal)
    if search:
        query = query.filter(Meal.name.ilike(f"%{search}%"))
    return query.offset(skip).limit(limit).all()

def create_meal(db: Session, meal: MealCreate) -> Meal:
    """創建新餐點"""
    db_meal = Meal(**meal.model_dump())
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal

def update_meal(db: Session, meal_id: int, meal: MealUpdate) -> Optional[Meal]:
    """更新餐點"""
    db_meal = get_meal(db, meal_id)
    if not db_meal:
        return None
    
    update_data = meal.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_meal, field, value)
    
    db.commit()
    db.refresh(db_meal)
    return db_meal

def delete_meal(db: Session, meal_id: int) -> bool:
    """刪除餐點"""
    db_meal = get_meal(db, meal_id)
    if not db_meal:
        return False
    
    db.delete(db_meal)
    db.commit()
    return True 