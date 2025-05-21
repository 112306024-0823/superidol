"""食物服務模塊"""
from typing import Optional, List
from datetime import datetime
from ..database.models import FoodItem
from ..extensions import db
from ..schemas.food_item import FoodItemCreate, FoodItemUpdate
from app.db import get_db_connection

class FoodService:
    @staticmethod
    def get_food_by_id(food_id: int) -> Optional[FoodItem]:
        """根據 ID 獲取食物"""
        return FoodItem.query.get(food_id)

    @staticmethod
    def get_foods() -> List[FoodItem]:
        """獲取所有食物"""
        return FoodItem.query.all()

    @staticmethod
    def create_food(food_data: FoodItemCreate) -> FoodItem:
        """創建新食物"""
        food = FoodItem(**food_data.dict())
        db.session.add(food)
        db.session.commit()
        return food

    @staticmethod
    def update_food(food: FoodItem, food_data: FoodItemUpdate) -> FoodItem:
        """更新食物信息"""
        for key, value in food_data.dict(exclude_unset=True).items():
            setattr(food, key, value)
        food.updated_at = datetime.utcnow()
        db.session.commit()
        return food

    @staticmethod
    def delete_food(food: FoodItem) -> None:
        """刪除食物"""
        db.session.delete(food)
        db.session.commit()

def search_food(filters):
    """
    搜尋符合條件的食物清單
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 基本查詢
            sql = """
                SELECT 
                    f.FoodID,
                    f.Name,
                    CAST(f.Calories AS FLOAT),
                    f.Price,
                    f.Set_Type,
                    r.Name AS Restaurant
                FROM Food f
                LEFT JOIN Restaurant r ON f.RestaurantID = r.RestaurantID
                WHERE 1 = 1
            """
            params = []

            # 添加過濾條件
            if filters.get('priceMin') and filters['priceMin'].strip():
                sql += " AND f.Price >= %s"
                params.append(float(filters['priceMin']))

            if filters.get('priceMax') and filters['priceMax'].strip():
                sql += " AND f.Price <= %s"
                params.append(float(filters['priceMax']))

            if filters.get('calMin') and filters['calMin'].strip():
                sql += " AND f.Calories >= %s"
                params.append(float(filters['calMin']))

            if filters.get('calMax') and filters['calMax'].strip():
                sql += " AND f.Calories <= %s"
                params.append(float(filters['calMax']))

            if filters.get('name') and filters['name'].strip():
                sql += " AND f.Name LIKE %s"
                params.append(f"%{filters['name']}%")

            if filters.get('restaurant') and filters['restaurant'].strip():
                sql += " AND r.Name LIKE %s"
                params.append(f"%{filters['restaurant']}%")

            if filters.get('type') and filters['type'].strip():
                sql += " AND f.Set_Type = %s"
                params.append(filters['type'])

            print(f"Executing SQL: {sql}")  # 添加 SQL 日誌
            print(f"Parameters: {params}")  # 添加參數日誌
            
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            
            # 將資料庫結果轉換為 JSON 格式
            results = []
            for row in rows:
                results.append({
                    'id': row[0],
                    'name': row[1],
                    'calories': float(row[2]) if row[2] is not None else 0,
                    'price': row[3],
                    'type': row[4],
                    'restaurant': row[5] or ''  # 處理 NULL 值
                })
            
            print(f"Found {len(results)} results")  # 添加結果數量日誌
            return results

    except Exception as e:
        print(f"Database error in search_food: {str(e)}")  # 添加錯誤日誌
        raise Exception(f"Database error: {str(e)}")
    finally:
        conn.close()

def add_food_record(user_id, food_data):
    """
    Add a food consumption record.
    
    Args:
        user_id (int): User ID
        food_data (dict): Food record data
        
    Returns:
        dict: Result of the operation
    """
    # TODO: Implement food record creation
    return {}

def get_user_favorites(user_id):
    """
    Get user's favorite foods.
    
    Args:
        user_id (int): User ID
        
    Returns:
        list: User's favorite foods
    """
    # TODO: Implement favorites retrieval
    return []

def add_to_favorites(user_id, food_id):
    """
    Add a food to user's favorites.
    
    Args:
        user_id (int): User ID
        food_id (int): Food ID
        
    Returns:
        dict: Result of the operation
    """
    # TODO: Implement add to favorites
    return {}

def remove_from_favorites(user_id, food_id):
    """
    Remove a food from user's favorites.
    
    Args:
        user_id (int): User ID
        food_id (int): Food ID
        
    Returns:
        dict: Result of the operation
    """
    # TODO: Implement remove from favorites
    return {} 