import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """基礎配置"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # 數據庫配置
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///super_idol.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CORS 配置
    CORS_ORIGINS = ['http://localhost:3000']  # 前端開發服務器

class DevelopmentConfig(Config):
    """開發環境配置"""
    DEBUG = True

class ProductionConfig(Config):
    """生產環境配置"""
    DEBUG = False
    
    # 生產環境特定的配置
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '').split(',')

class TestingConfig(Config):
    """測試環境配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:' 