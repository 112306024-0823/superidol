"""
資料庫初始化腳本 - 創建所需的表格並填充初始數據
"""
import sys
import os
import logging

# 設置路徑
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from app.db import get_db_connection

# 配置日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def init_exercise_items():
    """初始化運動項目表"""
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 檢查表是否存在
            cursor.execute("SHOW TABLES LIKE 'ExerciseItem'")
            if not cursor.fetchone():
                logger.info("創建 ExerciseItem 表")
                cursor.execute("""
                CREATE TABLE ExerciseItem (
                    Exercise_Name VARCHAR(50) PRIMARY KEY,
                    MET DECIMAL(5,2) NOT NULL,
                    Status ENUM('active', 'inactive') DEFAULT 'active'
                )
                """)
            
            # 檢查表中是否有數據
            cursor.execute("SELECT COUNT(*) as count FROM ExerciseItem")
            if cursor.fetchone()['count'] == 0:
                logger.info("填充 ExerciseItem 表初始數據")
                # 插入運動項目數據
                exercise_items = [
                    ('籃球', 7.0), ('快走', 4.0), ('騎腳踏車', 6.0), ('健走', 6.0),
                    ('伏地挺身', 5.0), ('攀岩', 8.0), ('划船', 7.0), ('跑步(8km/hr)', 8.0),
                    ('跑步(10km/hr)', 10.0), ('足球', 7.0), ('游泳', 7.0), ('打太極', 4.0),
                    ('慢走', 3.0), ('瑜珈', 5.0)
                ]
                
                for name, met in exercise_items:
                    cursor.execute(
                        "INSERT IGNORE INTO ExerciseItem (Exercise_Name, MET) VALUES (%s, %s)",
                        (name, met)
                    )
                
                conn.commit()
                logger.info(f"已插入 {len(exercise_items)} 筆運動項目數據")
            else:
                logger.info("ExerciseItem 表已存在且包含數據")
                
            # 顯示現有數據
            cursor.execute("SELECT * FROM ExerciseItem")
            items = cursor.fetchall()
            logger.info(f"ExerciseItem 表中有 {len(items)} 筆數據")
            for item in items:
                logger.info(f"  - {item['Exercise_Name']}: MET={item['MET']}")
                
    except Exception as e:
        conn.rollback()
        logger.error(f"初始化 ExerciseItem 表失敗: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        conn.close()

def main():
    """主函數 - 初始化所有表"""
    try:
        logger.info("開始初始化資料庫...")
        init_exercise_items()
        logger.info("資料庫初始化完成")
    except Exception as e:
        logger.error(f"資料庫初始化過程中發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 