from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from dotenv import load_dotenv
import os
from .config import Config
from .extensions import jwt, cors
from .errors.handlers import register_error_handlers
from .api.v1 import auth, users

# 載入環境變數
load_dotenv()

# 初始化擴展
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    """創建 Flask 應用程序"""
    app = Flask(__name__)
    
    # 配置
    app.config.from_object(config_class)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # 初始化擴展
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    jwt.init_app(app)
    cors.init_app(app)
    
    # 註冊錯誤處理器
    register_error_handlers(app)
    
    # 註冊藍圖
    app.register_blueprint(auth.bp, url_prefix='/api/v1/auth')
    app.register_blueprint(users.bp, url_prefix='/api/v1/users')
    
    # 創建數據庫表
    with app.app_context():
        db.create_all()
    
    return app 