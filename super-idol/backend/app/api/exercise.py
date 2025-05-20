"""
Exercise API endpoints.
"""

from flask import Blueprint, request, jsonify
from app.services.exercise_service import log_exercise, get_exercise_records

exercise_bp = Blueprint('exercise', __name__)

@exercise_bp.route('/log', methods=['POST'])
def log_exercise_api():
    """
    新增一筆運動紀錄。
    Request body:
      exercise_name: 運動名稱
      duration: 持續時間（分鐘）
      date: 運動日期
    """
    try:
        data = request.get_json() or {}
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({"error": "user_id 為必填欄位"}), 400
        result = log_exercise(user_id, data)
        if 'error' in result:
            return jsonify(result), 400
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@exercise_bp.route('/records', methods=['GET'])
def get_exercise_records_api():
    """
    查詢使用者的運動紀錄。
    Query params:
      user_id: 使用者ID
      start_date: 起始日期（可選）
      end_date: 結束日期（可選）
    """
    try:
        user_id = request.args.get('user_id', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        if not user_id:
            return jsonify({"error": "user_id 為必填欄位"}), 400
        records = get_exercise_records(user_id, start_date, end_date)
        return jsonify({"records": records}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@exercise_bp.route('/preferences', methods=['GET', 'POST'])
def manage_exercise_preferences():
    """
    Manage user's exercise preferences.
    ---
    Methods:
      GET: Get user's exercise preferences
      POST: Set exercise preferences
    Responses:
      200:
        description: Operation successful
    """
    # TODO: Implement exercise preferences management
    return jsonify({"message": "Exercise preferences endpoint - to be implemented"}), 200 