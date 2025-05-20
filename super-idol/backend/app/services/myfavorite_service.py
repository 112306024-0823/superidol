from app.db import get_db_connection

def add_to_favorite(user_id, food_id):
    if not isinstance(user_id, int) or not isinstance(food_id, int):
        return {"error": "user_id and food_id must be integers"}, 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM Users WHERE UserID = %s", (user_id,))
        if cursor.fetchone() is None:
            return {"error": f"User {user_id} not found"}, 404

        cursor.execute("SELECT 1 FROM Food WHERE FoodID = %s", (food_id,))
        if cursor.fetchone() is None:
            return {"error": f"Food {food_id} not found"}, 404

        cursor.execute("SELECT 1 FROM MyFavorite WHERE UserID = %s AND FoodID = %s", (user_id, food_id))
        if cursor.fetchone() is not None:
            return {"message": "Food already in favorites"}, 200

        cursor.execute("INSERT INTO MyFavorite (UserID, FoodID) VALUES (%s, %s)", (user_id, food_id))
        conn.commit()
        return {"message": "Food added to favorites successfully"}, 201

    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500

    finally:
        cursor.close()
        conn.close()
