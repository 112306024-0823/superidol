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

def get_exercise_preferences(user_id: int) -> List[str]:
    """
    查詢使用者的運動偏好。
    Args:
        user_id (int): 使用者ID
    Returns:
        list: 運動偏好名稱列表
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT Exercise_Name FROM Exercise_Preference WHERE UserID = %s", (user_id,))
            prefs = [row['Exercise_Name'] for row in cursor.fetchall()]
        return prefs
    except Exception as e:
        return []
    finally:
        conn.close()

def set_exercise_preferences(user_id: int, preferences: List[str]) -> Dict[str, Any]:
    """
    設定使用者的運動偏好（會先清空再新增）。
    Args:
        user_id (int): 使用者ID
        preferences (list): 運動名稱列表
    Returns:
        dict: 結果訊息
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 先刪除舊有偏好
            cursor.execute("DELETE FROM Exercise_Preference WHERE UserID = %s", (user_id,))
            # 新增新偏好
            for exercise_name in preferences:
                cursor.execute("SELECT 1 FROM ExerciseItem WHERE Exercise_Name = %s", (exercise_name,))
                if cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO Exercise_Preference (UserID, Exercise_Name) VALUES (%s, %s)",
                        (user_id, exercise_name)
                    )
            conn.commit()
        return {"message": "運動偏好已更新"}
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        conn.close()

def delete_exercise_record(user_id: int, record_id: int) -> Dict[str, Any]:
    """
    刪除一筆運動紀錄。
    Args:
        user_id (int): 使用者ID
        record_id (int): 運動紀錄ID
    Returns:
        dict: 結果訊息
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "DELETE FROM Exercise_Records WHERE UserID = %s AND RecordID = %s",
                (user_id, record_id)
            )
            conn.commit()
        return {"message": "運動紀錄已刪除"}
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        conn.close()

def update_exercise_record(user_id: int, record_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    更新一筆運動紀錄（可更新運動名稱、時長、日期）。
    Args:
        user_id (int): 使用者ID
        record_id (int): 運動紀錄ID
        update_data (dict): 欲更新欄位
    Returns:
        dict: 結果訊息
    """
    allowed_fields = {'exercise_name', 'duration', 'date'}
    fields = []
    params = []
    for key in allowed_fields:
        if key in update_data:
            if key == 'exercise_name':
                fields.append('Exercise_Name = %s')
            elif key == 'duration':
                fields.append('Duration = %s')
            elif key == 'date':
                fields.append('Date = %s')
            params.append(update_data[key])
    if not fields:
        return {"error": "沒有可更新的欄位"}
    params.extend([user_id, record_id])
    sql = f"UPDATE Exercise_Records SET {', '.join(fields)} WHERE UserID = %s AND RecordID = %s"
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, tuple(params))
            conn.commit()
        return {"message": "運動紀錄已更新"}
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        conn.close() 