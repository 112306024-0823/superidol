from flask import Blueprint, request, jsonify
from app.services.myfavorite_service import add_to_favorite

my_favorite_bp = Blueprint('my_favorite', __name__)

@my_favorite_bp.route('/favorite', methods=['POST'])
def add_favorite():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        user_id = data.get('user_id')
        food_id = data.get('food_id')

        # 參數基本驗證
        if not isinstance(user_id, int) or not isinstance(food_id, int):
            return jsonify({"error": "user_id and food_id must be integers"}), 400

        result, status = add_to_favorite(user_id, food_id)
        return jsonify(result), status

    except Exception as e:
        return jsonify({"error": str(e)}), 500

