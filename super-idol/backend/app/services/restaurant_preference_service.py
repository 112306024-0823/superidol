from app.db import get_db_connection

def insert_restaurant_preference(user_id, restaurant_id):
    """
    插入一筆使用者的餐廳偏好（由註冊流程中使用）
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 確認餐廳是否存在
        cursor.execute("SELECT * FROM Restaurant WHERE RestuarantID = %s", (restaurant_id,))
        restaurant = cursor.fetchone()
        if not restaurant:
            return {"error": f"Restaurant ID {restaurant_id} not found"}

        # 新增偏好關係
        cursor.execute("""
            INSERT INTO Restaurant_Preference (UserID, RestuarantID)
            VALUES (%s, %s)
        """, (user_id, restaurant_id))

        conn.commit()
        return {"message": f"Preference for restaurant {restaurant_id} added"}

    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        conn.close()
