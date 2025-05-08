"""
Initialization file for the Flask application.
"""

import os
import logging
from flask import Flask
from flask_cors import CORS

def create_app():
    # 根據環境選擇正確的配置
    env = os.getenv('FLASK_ENV', 'development')
    
    if env == 'production':
        from app.config import ProductionConfig as AppConfig
        logging.info("使用生產環境配置")
    elif env == 'testing':
        from app.config import TestingConfig as AppConfig
        logging.info("使用測試環境配置")
    else:
        from app.config import DevelopmentConfig as AppConfig
        logging.info("使用開發環境配置")
    
    app = Flask(__name__)
    app.config.from_object(AppConfig)
    
    # 配置日誌級別
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    logging.basicConfig(level=getattr(logging, log_level))
    
    # 設置CORS，使用配置中的origins
    CORS(app, resources={r"/api/*": {"origins": app.config.get('CORS_ORIGINS', '*')}})
    
    # 註冊藍圖
    from app.api import auth_bp, food_bp, exercise_bp, report_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(food_bp, url_prefix='/api/food')
    app.register_blueprint(exercise_bp, url_prefix='/api/exercise')
    app.register_blueprint(report_bp, url_prefix='/api/report')
    
    # 記錄應用啟動信息
    logging.info(f"Flask應用已啟動，環境: {env}")
    logging.info(f"數據庫連接: {app.config.get('MYSQL_HOST')}:{app.config.get('MYSQL_PORT')}")
    logging.info(f"CORS設置: {app.config.get('CORS_ORIGINS')}")
    
    return app 