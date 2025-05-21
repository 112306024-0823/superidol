from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user
from app.db import get_db_connection
import jwt
from app.config import Config

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json() or {}

        required_fields = ['name', 'email', 'password', 'weight', 'budget', 'weekcalorielimit']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        result = register_user(data)
        if 'error' in result:
            return jsonify(result), 409 if 'exists' in result['error'] else 400

        login_result = login_user({"email": data['email'], "password": data['password']})
        if 'error' in login_result:
            return jsonify({"error": "Registration succeeded but login failed"}), 500

        return jsonify(login_result), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400
            
        # Call the service function to login user 

        result = login_user(data)
        if 'error' in result:
            return jsonify(result), 401

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@auth_bp.route('/user', methods=['GET'])
def get_user():
    """獲取用戶完整資料"""
    try:
        # 從 Authorization Header 獲取 token
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid token"}), 401
            
        token = auth_header.split(' ')[1]
        
        try:
            # 解碼 token
            payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')
            
            # 獲取用戶資料
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT UserID, Name, Email, Weight, Budget, WeekCalorieLimit 
                    FROM Users 
                    WHERE UserID = %s
                """, (user_id,))
                user = cursor.fetchone()
                
            if not user:
                return jsonify({"error": "User not found"}), 404
                
            # 返回完整用戶資料
            return jsonify({
                "id": user['UserID'],
                "name": user['Name'],
                "email": user['Email'],
                "weight": user['Weight'],
                "budget": user['Budget'],
                "weekCalorieLimit": user['WeekCalorieLimit']
            }), 200
            
        except jwt.PyJWTError:
            return jsonify({"error": "Invalid or expired token"}), 401
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500
