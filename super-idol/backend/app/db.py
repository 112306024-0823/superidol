"""
檔案：db.py
用途：資料庫連接與操作工具
"""

import pymysql
import os
import sys

# 直接從檔案中導入 Config 類
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
from config import Config



def get_db_connection():
    """
    獲取資料庫連接
    
    Returns:
        pymysql.connections.Connection: 資料庫連接對象
    """
    try:
        return pymysql.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            db=Config.MYSQL_DB,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        print(f"資料庫連接失敗: {str(e)}")
        raise

def execute_query(query, params=None):
    """
    執行資料查詢操作
    
    Args:
        query (str): SQL 查詢語句
        params (tuple, optional): 查詢參數
        
    Returns:
        list: 查詢結果
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            result = cursor.fetchall()
        return result
    finally:
        conn.close()

def execute_update(query, params=None):
    """
    執行資料更新操作（INSERT, UPDATE, DELETE）
    
    Args:
        query (str): SQL 更新語句
        params (tuple, optional): 更新參數
        
    Returns:
        int: 受影響的行數
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            affected_rows = cursor.execute(query, params or ())
        conn.commit()
        return affected_rows
    except Exception as e:
        conn.rollback()
        print(f"執行更新操作失敗: {str(e)}")
        raise
    finally:
        conn.close()

def execute_transaction(queries_and_params):
    """
    在單一事務中執行多個操作
    
    Args:
        queries_and_params (list): 包含 (query, params) 元組的列表
        
    Returns:
        bool: 事務是否成功執行
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            for query, params in queries_and_params:
                cursor.execute(query, params or ())
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"執行事務失敗: {str(e)}")
        raise
    finally:
        conn.close() 
        