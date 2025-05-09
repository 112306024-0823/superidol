"""
Authentication API endpoints.
"""

from flask import Blueprint, request, jsonify
from app.db import get_db_connection
from app.services.auth_service import register_user, login_user

auth_bp = Blueprint('auth', __name__)



#註冊
@auth_bp.route('/signup', methods=['POST'])
def signup():
    """
    Register a new user and return JWT access token.
    ---
    Request body:
      name: User's name
      email: User's email
      password: User's password
    Responses:
      201:
        description: User registered successfully
      400:
        description: Invalid input data
      409:
        description: Email already exists
    """
    try:
        data = request.get_json() or {}
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        if not all([name, email, password]):
            return jsonify({"error": "Name, email, and password are required"}), 400

        # 註冊使用者
        result = register_user(data)
        if 'error' in result:
            status_code = 409 if 'already exists' in result['error'] else 400
            return jsonify(result), status_code

        # 註冊成功後，直接登入並產生 JWT Token
        login_result = login_user({"email": email, "password": password})
        if 'error' in login_result:
            return jsonify({"error": "Registration succeeded but login failed"}), 500

        # 回傳 access_token 與使用者資訊
        return jsonify(login_result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#登入
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login a user.
    ---
    Request body:
      email: User's email
      password: User's password
    Responses:
      200:
        description: User logged in successfully
      400:
        description: Invalid input data
      401:
        description: Invalid credentials
    """
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