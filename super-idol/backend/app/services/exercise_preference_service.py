from app.db import get_db_connection

def insert_exercise_preference(user_id, exercise_name):
    """
    插入一筆使用者的運動偏好（由註冊流程使用）
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # 檢查該運動名稱是否存在於 ExerciseItem
        cursor.execute("SELECT * FROM ExerciseItem WHERE Exercise_Name = %s", (exercise_name,))
        item = cursor.fetchone()
        if not item:
            return {"error": f"Exercise '{exercise_name}' not found"}

        # 插入偏好
        cursor.execute("""
            INSERT INTO Exercise_Preference (UserID, Exercise_Name)
            VALUES (%s, %s)
        """, (user_id, exercise_name))

        conn.commit()
        return {"message": f"Preference for exercise '{exercise_name}' added"}

    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        conn.close()
