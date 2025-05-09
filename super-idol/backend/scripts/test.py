"""
檔案：test_db.py
用途：直接測試資料庫連接，無需導入其他模組
"""

import pymysql

# 資料庫連接資訊（直接硬編碼，僅用於測試）
DB_HOST = 'superidol.c9i82eygu8mk.ap-southeast-2.rds.amazonaws.com'
DB_PORT = 3306
DB_USER = 'DBMS11302'
DB_PASSWORD = 'ilovedbms'
DB_NAME = 'superidol'

def test_connection():
    """
    測試資料庫連接是否正常
    """
    try:
        # 創建資料庫連接
        conn = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            db=DB_NAME,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        
        # 測試連接
        with conn.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"資料庫連接成功！")
            print(f"資料庫版本: {version['VERSION()']}")
        
        # 關閉連接
        conn.close()
        return True
    except Exception as e:
        print(f"資料庫連接失敗: {str(e)}")
        return False

if __name__ == "__main__":
    print("正在測試資料庫連接...")
    test_connection() 