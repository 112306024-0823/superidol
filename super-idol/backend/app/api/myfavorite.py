from flask import Blueprint, request, jsonify
from app.services.myfavorite_service import add_to_favorite, remove_from_favorite, get_favorites_by_user
import traceback

my_favorite_bp = Blueprint('my_favorite', __name__)

@my_favorite_bp.route('/favorites', methods=['POST'])
def add_favorite():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        print(f"收到新增收藏請求: {data}")  # 調試用
        
        user_id = data.get('user_id')
        food_id = data.get('food_id')

        # 驗證參數
        if user_id is None or food_id is None:
            return jsonify({"error": "user_id and food_id are required"}), 400
            
        if not isinstance(user_id, int) or not isinstance(food_id, int):
            return jsonify({"error": "user_id and food_id must be integers"}), 400

        result, status = add_to_favorite(user_id, food_id)
        print(f"新增收藏結果: {result}, 狀態: {status}")  # 調試用
        return jsonify(result), status

    except Exception as e:
        print(f"新增收藏發生錯誤: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@my_favorite_bp.route('/favorites', methods=['DELETE'])
def delete_favorite():
    try:
        if not request.is_json:
            return jsonify({"error": "Request must be JSON"}), 400

        data = request.get_json()
        print(f"收到刪除收藏請求: {data}")  # 調試用
        
        user_id = data.get('user_id')
        food_id = data.get('food_id')

        # 驗證參數
        if user_id is None or food_id is None:
            return jsonify({"error": "user_id and food_id are required"}), 400
            
        if not isinstance(user_id, int) or not isinstance(food_id, int):
            return jsonify({"error": "user_id and food_id must be integers"}), 400

        result, status = remove_from_favorite(user_id, food_id)
        print(f"刪除收藏結果: {result}, 狀態: {status}")  # 調試用
        return jsonify(result), status

    except Exception as e:
        print(f"刪除收藏發生錯誤: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@my_favorite_bp.route('/favorites', methods=['GET'])
def get_favorites():
    try:
        user_id = request.args.get('user_id', type=int)
        print(f"收到獲取收藏請求，user_id: {user_id}")  # 調試用
        
        if not user_id:
            return jsonify({"error": "user_id query parameter is required"}), 400

        favorites, status = get_favorites_by_user(user_id)
        print(f"獲取收藏結果: {len(favorites) if isinstance(favorites, list) else 'error'}, 狀態: {status}")  # 調試用
        return jsonify(favorites), status

    except Exception as e:
        print(f"獲取收藏發生錯誤: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500