from flask import Blueprint, request, jsonify
from app.services.auth_service import register_user, login_user

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

        result = login_user(data)
        if 'error' in result:
            return jsonify(result), 401

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
