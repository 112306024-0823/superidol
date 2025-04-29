"""
檔案：test_db.py
用途：測試資料庫連接
功能：
- 測試資料庫連接是否正常
- 顯示資料庫版本
- 顯示資料表列表
"""

from sqlalchemy import text
from config.database import engine

def test_connection():
    """
    測試資料庫連接
    
    Returns:
        bool: 連接是否成功
    """
    try:
        # 測試連接
        with engine.connect() as connection:
            # 獲取資料庫版本
            result = connection.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"資料庫版本: {version}")
            
            # 獲取資料表列表
            result = connection.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            tables = [row[0] for row in result]
            print(f"資料表列表: {tables}")
            
            return True
    except Exception as e:
        print(f"連接失敗: {str(e)}")
        return False

if __name__ == "__main__":
    print("開始測試資料庫連接...")
    if test_connection():
        print("資料庫連接成功！")
    else:
        print("資料庫連接失敗！") 