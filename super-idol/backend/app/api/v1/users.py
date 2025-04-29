from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .. import db
from ..models.user import User
from . import bp
from ...services.user_service import UserService
from ...schemas.user import UserResponse, UserUpdate
from ..deps import get_current_user

bp = Blueprint('users', __name__)

@bp.route('/users/me', methods=['GET'])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'favorite_idols': [idol.id for idol in user.favorite_idols]
    })

@bp.route('/users/me/favorite_idols', methods=['GET'])
@jwt_required()
def get_favorite_idols():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    return jsonify([{
        'id': idol.id,
        'name': idol.name,
        'birthday': idol.birthday.isoformat(),
        'height': idol.height,
        'weight': idol.weight,
        'blood_type': idol.blood_type,
        'hobbies': idol.hobbies,
        'specialties': idol.specialties,
        'description': idol.description
    } for idol in user.favorite_idols])

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user_info():
    """獲取當前用戶信息"""
    user = get_current_user()
    return jsonify(UserResponse.from_orm(user).dict())

@bp.route('/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    """更新當前用戶信息"""
    user = get_current_user()
    data = request.get_json()
    user_data = UserUpdate(**data)
    
    updated_user = UserService.update_user(user, user_data)
    return jsonify(UserResponse.from_orm(updated_user).dict())

@bp.route('/me', methods=['DELETE'])
@jwt_required()
def delete_current_user():
    """刪除當前用戶"""
    user = get_current_user()
    UserService.delete_user(user)
    return jsonify({'message': 'User deleted successfully'}) 