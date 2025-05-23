from app.db import get_db_connection
import traceback

def add_to_favorite(user_id, food_id):
    if not isinstance(user_id, int) or not isinstance(food_id, int):
        return {"error": "user_id and food_id must be integers"}, 400

    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 檢查用戶是否存在
        cursor.execute("SELECT 1 FROM Users WHERE UserID = %s", (user_id,))
        if cursor.fetchone() is None:
            return {"error": f"User {user_id} not found"}, 404

        # 檢查食物是否存在
        cursor.execute("SELECT 1 FROM Food WHERE FoodID = %s", (food_id,))
        if cursor.fetchone() is None:
            return {"error": f"Food {food_id} not found"}, 404

        # 檢查是否已經收藏
        cursor.execute("SELECT 1 FROM MyFavorite WHERE UserID = %s AND FoodID = %s", (user_id, food_id))
        if cursor.fetchone() is not None:
            return {"message": "Food already in favorites"}, 200

        # 新增收藏 (確保欄位順序正確：FoodID, UserID)
        cursor.execute("INSERT INTO MyFavorite (FoodID, UserID) VALUES (%s, %s)", (food_id, user_id))
        conn.commit()
        return {"message": "Food added to favorites successfully"}, 201

    except Exception as e:
        traceback.print_exc()  # 印出完整錯誤堆疊方便調試
        if conn:
            conn.rollback()
        return {"error": str(e)}, 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def remove_from_favorite(user_id, food_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 檢查收藏是否存在
        cursor.execute("SELECT 1 FROM MyFavorite WHERE UserID = %s AND FoodID = %s", (user_id, food_id))
        if cursor.fetchone() is None:
            return {"error": "Favorite not found"}, 404

        # 刪除收藏
        cursor.execute("DELETE FROM MyFavorite WHERE UserID = %s AND FoodID = %s", (user_id, food_id))
        conn.commit()
        return {"message": "Favorite removed successfully"}, 200

    except Exception as e:
        if conn:
            conn.rollback()
        return {"error": str(e)}, 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def get_favorites_by_user(user_id):
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # 使用 dictionary cursor 回傳方便的 dict

        # 修改查詢，確保欄位名稱與前端一致
        cursor.execute("""
            SELECT f.FoodID as id, f.Name as name, f.Calories as calories, f.Price as price,
                   f.Type as type, f.FoodType as food_type, f.Restaurant as restaurant
            FROM MyFavorite mf
            JOIN Food f ON mf.FoodID = f.FoodID
            WHERE mf.UserID = %s
            ORDER BY f.Name
        """, (user_id,))

        favorites = cursor.fetchall()
        return favorites, 200

    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}, 500

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()