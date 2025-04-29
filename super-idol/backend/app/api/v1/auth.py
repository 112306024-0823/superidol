from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from ...services.user_service import UserService
from ...utils.security import verify_password, create_token
from ...schemas.user import UserCreate, UserResponse

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['POST'])
def register():
    """註冊新用戶"""
    data = request.get_json()
    user_data = UserCreate(**data)
    
    # 檢查用戶名是否已存在
    if UserService.get_user_by_username(user_data.username):
        return jsonify({'error': 'Username already exists'}), 400
    
    # 檢查郵箱是否已存在
    if UserService.get_user_by_email(user_data.email):
        return jsonify({'error': 'Email already exists'}), 400
    
    # 創建用戶
    user = UserService.create_user(user_data)
    
    # 創建訪問令牌
    access_token = create_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'user': UserResponse.from_orm(user).dict()
    }), 201

@bp.route('/login', methods=['POST'])
def login():
    """用戶登錄"""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    user = UserService.get_user_by_username(username)
    if not user or not verify_password(password, user.password_hash):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # 創建訪問令牌
    access_token = create_token(identity=user.id)
    
    return jsonify({
        'access_token': access_token,
        'user': UserResponse.from_orm(user).dict()
    }) 