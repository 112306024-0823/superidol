"""
Food API endpoints.
"""

from flask import Blueprint, request, jsonify
from ..services.food_service import search_food
from flask_cors import CORS

food_bp = Blueprint('food', __name__)
CORS(food_bp)  # 啟用 CORS

@food_bp.route('/', methods=['GET'])
def get_foods():
    """
    Get all foods or search for foods based on filters
    """
    try:
        # 初始化空的過濾條件
        filters = {
            'name': request.args.get('name', ''),
            'priceMin': request.args.get('priceMin', ''),
            'priceMax': request.args.get('priceMax', ''),
            'calMin': request.args.get('calMin', ''),
            'calMax': request.args.get('calMax', ''),
            'type': request.args.get('type', ''),
            'restaurant': request.args.get('restaurant', '')
        }

        results = search_food(filters)
        if not results:
            results = []  # 確保返回空列表而不是 None
        return jsonify(results), 200
    except Exception as e:
        print(f"Error in get_foods: {str(e)}")  # 添加服務器端日誌
        return jsonify({'error': str(e)}), 500

@food_bp.route('/record', methods=['POST'])
def add_food_record():
    """
    Add a food consumption record.
    ---
    Request body:
      food_id: ID of the food
      date: Date of consumption
      meal_time: Time of meal (breakfast, lunch, dinner, supper)
    Responses:
      201:
        description: Food record created successfully
    """
    # TODO: Implement food record creation
    return jsonify({"message": "Add food record endpoint - to be implemented"}), 201

@food_bp.route('/favorites', methods=['GET', 'POST', 'DELETE'])
def manage_favorites():
    """
    Manage user's favorite foods.
    ---
    Methods:
      GET: Get user's favorite foods
      POST: Add a food to favorites
      DELETE: Remove a food from favorites
    Responses:
      200:
        description: Operation successful
    """
    # TODO: Implement favorites management
    return jsonify({"message": "Favorites management endpoint - to be implemented"}), 200 