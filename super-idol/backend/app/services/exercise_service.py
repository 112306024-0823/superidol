"""
Exercise service functions.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from app.db import get_db_connection

def log_exercise(user_id: int, exercise_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    新增一筆運動紀錄，並自動計算消耗熱量。

    Args:
        user_id (int): 使用者ID
        exercise_data (dict): 運動資料，需包含 exercise_name, duration, date

    Returns:
        dict: 新增結果與紀錄內容
    """
    exercise_name = exercise_data.get('exercise_name')
    duration = exercise_data.get('duration')
    date = exercise_data.get('date')
    if not all([exercise_name, duration, date]):
        return {"error": "exercise_name, duration, date 為必填欄位"}

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 查詢體重
            cursor.execute("SELECT Weight FROM Users WHERE UserID = %s", (user_id,))
            user = cursor.fetchone()
            if not user or user['Weight'] is None:
                return {"error": "找不到使用者或體重未設定"}
            weight = user['Weight']

            # 查詢 MET
            cursor.execute("SELECT MET FROM ExerciseItem WHERE Exercise_Name = %s", (exercise_name,))
            item = cursor.fetchone()
            if not item:
                return {"error": f"找不到運動名稱: {exercise_name}"}
            met = item['MET']

            # 計算消耗熱量
            calories_burned = met * 3.5 * weight / 200 * float(duration)

            # 寫入紀錄
            cursor.execute(
                """
                INSERT INTO Exercise_Records (UserID, Exercise_Name, Duration, Date)
                VALUES (%s, %s, %s, %s)
                """,
                (user_id, exercise_name, duration, date)
            )
            record_id = cursor.lastrowid
        conn.commit()
        return {
            "message": "運動紀錄新增成功",
            "record": {
                "record_id": record_id,
                "user_id": user_id,
                "exercise_name": exercise_name,
                "duration": duration,
                "date": date,
                "calories_burned": calories_burned
            }
        }
    except Exception as e:
        conn.rollback()
        return {"error": f"資料庫錯誤: {str(e)}"}
    finally:
        conn.close()

def get_exercise_records(user_id: int, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    查詢使用者的運動紀錄，並計算消耗熱量。

    Args:
        user_id (int): 使用者ID
        start_date (str, optional): 起始日期 (YYYY-MM-DD)
        end_date (str, optional): 結束日期 (YYYY-MM-DD)

    Returns:
        list: 運動紀錄列表
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 查詢體重
            cursor.execute("SELECT Weight FROM Users WHERE UserID = %s", (user_id,))
            user = cursor.fetchone()
            if not user or user['Weight'] is None:
                return []
            weight = user['Weight']

            # 查詢紀錄
            sql = "SELECT RecordID, Exercise_Name, Duration, Date FROM Exercise_Records WHERE UserID = %s"
            params = [user_id]
            if start_date:
                sql += " AND Date >= %s"
                params.append(start_date)
            if end_date:
                sql += " AND Date <= %s"
                params.append(end_date)
            sql += " ORDER BY Date DESC"
            cursor.execute(sql, tuple(params))
            records = cursor.fetchall()

            # 查詢所有運動名稱對應的 MET
            exercise_names = list({r['Exercise_Name'] for r in records})
            if exercise_names:
                format_strings = ','.join(['%s'] * len(exercise_names))
                cursor.execute(f"SELECT Exercise_Name, MET FROM ExerciseItem WHERE Exercise_Name IN ({format_strings})", tuple(exercise_names))
                met_map = {row['Exercise_Name']: row['MET'] for row in cursor.fetchall()}
            else:
                met_map = {}

            # 計算消耗熱量
            for r in records:
                met = met_map.get(r['Exercise_Name'], 0)
                r['calories_burned'] = met * 3.5 * weight / 200 * float(r['Duration'])
            return records
    except Exception as e:
        return []
    finally:
        conn.close()

def get_exercise_preferences(user_id):
    """
    Get user's exercise preferences.
    
    Args:
        user_id (int): User ID
        
    Returns:
        list: User's preferred exercises
    """
    # TODO: Implement preferences retrieval
    return []

def set_exercise_preferences(user_id, preferences):
    """
    Set user's exercise preferences.
    
    Args:
        user_id (int): User ID
        preferences (list): Exercise preferences
        
    Returns:
        dict: Result of the operation
    """
    # TODO: Implement setting preferences
    return {} 