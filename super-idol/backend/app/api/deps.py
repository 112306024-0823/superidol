from functools import lru_cache
from typing import Generator
from flask import current_app
from flask_jwt_extended import JWTManager, get_jwt_identity
from ..database.models import User
from ..services.user_service import UserService

jwt = JWTManager()

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    """JWT 用戶查找回調"""
    identity = jwt_data["sub"]
    return UserService.get_user_by_id(identity)

def get_current_user() -> User:
    """獲取當前用戶"""
    user_id = get_jwt_identity()
    return UserService.get_user_by_id(user_id)

@lru_cache()
def get_db() -> Generator:
    """獲取數據庫會話"""
    db = current_app.extensions['sqlalchemy'].db
    try:
        yield db.session
    finally:
        db.session.close() 