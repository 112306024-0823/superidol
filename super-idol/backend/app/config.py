"""
Configuration settings for the application.
"""

import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-please-change-in-production')
    DEBUG = False
    
    # Database settings
    MYSQL_HOST = os.getenv('DB_HOST', 'superidol.c9i82eygu8mk.ap-southeast-2.rds.amazonaws.com')
    MYSQL_PORT = int(os.getenv('DB_PORT', '3306'))
    MYSQL_USER = os.getenv('DB_USER', 'DBMS11302')
    MYSQL_PASSWORD = os.getenv('DB_PASSWORD', 'ilovedbms')
    MYSQL_DB = os.getenv('DB_NAME', 'superidol')
    
    # JWT settings
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-please-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_TOKEN_EXPIRE', '3600'))  # 1 hour
    
    # API settings
    API_TITLE = 'Super Idol API'
    API_VERSION = 'v1'
    
    # CORS 配置
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,https://super-idol.onrender.com').split(',')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    MYSQL_DB = 'super_idol_test_db'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    # 從環境變數獲取所有生產環境配置
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for production environment")
    
    # JWT 設置
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    if not JWT_SECRET_KEY:
        raise ValueError("No JWT_SECRET_KEY set for production environment")
    
    # 資料庫設置 - 必須從環境變數獲取
    MYSQL_HOST = os.getenv('DB_HOST')
    MYSQL_PORT = int(os.getenv('DB_PORT', '3306'))
    MYSQL_USER = os.getenv('DB_USER')
    MYSQL_PASSWORD = os.getenv('DB_PASSWORD')
    MYSQL_DB = os.getenv('DB_NAME')
    
    # 檢查必要的資料庫設置
    if not all([MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB]):
        raise ValueError("Database configuration incomplete. Check environment variables.")
    
    # 生產環境 CORS 設置
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'https://super-idol.onrender.com').split(',') 