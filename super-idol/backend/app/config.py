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
    SECRET_KEY = 'dev-key-please-change-in-production'
    DEBUG = False
    
    # Database settings
    MYSQL_HOST = 'superidol.c9i82eygu8mk.ap-southeast-2.rds.amazonaws.com'
    MYSQL_PORT = 3306
    MYSQL_USER = 'DBMS11302'
    MYSQL_PASSWORD = 'ilovedbms'
    MYSQL_DB = 'superidol'
    
    # JWT settings
    JWT_SECRET_KEY = 'jwt-secret-key-please-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    
    # API settings
    API_TITLE = 'Super Idol API'
    API_VERSION = 'v1'
    
    # CORS 配置
    CORS_ORIGINS = ['http://localhost:3000']  # 前端開發服務器

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
    # In production, these values should be set through environment variables
    
    # 生產環境特定的配置
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '').split(',') 