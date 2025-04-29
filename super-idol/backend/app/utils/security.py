import bcrypt
from typing import Union
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token

def get_password_hash(password: str) -> str:
    """生成密碼哈希"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """驗證密碼"""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

def create_token(identity: Union[int, str], expires_delta: timedelta = None) -> str:
    """創建 JWT token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=1)
    
    return create_access_token(
        identity=identity,
        expires_delta=expires_delta
    ) 