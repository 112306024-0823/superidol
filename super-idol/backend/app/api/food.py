"""
Food API endpoints.
"""

from flask import Blueprint, request, jsonify
from ..services.food_service import (
    search_food, 
    add_food_record, 
    get_user_food_records,
    delete_food_record, 
    get_user_favorites, 
    add_to_favorites, 
    remove_from_favorites,
    update_food_record as update_food_record_service
)
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
def create_food_record():
    """
    添加食物消費記錄
    ---
    請求參數:
      user_id: 用戶ID
      food_id: 食物ID
      mealtime: 餐點類型 (早餐/午餐/晚餐/宵夜)
      quantity: 數量
      date: 日期 (YYYY-MM-DD)
    回應:
      201: 記錄創建成功
    """
    try:
        data = request.json
        
        # 檢查必要參數
        if 'user_id' not in data:
            return jsonify({"error": "Missing required field: user_id"}), 400
            
        result = add_food_record(data['user_id'], data)
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@food_bp.route('/record', methods=['GET'])
def get_food_records():
    """
    獲取用戶食物記錄
    ---
    查詢參數:
      user_id: 用戶ID
      start_date: 開始日期 (可選)
      end_date: 結束日期 (可選)
      mealtime: 餐點類型 (可選)
    回應:
      200: 食物記錄列表
    """
    try:
        user_id = request.args.get('user_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        mealtime = request.args.get('mealtime')
        
        if not user_id:
            return jsonify({"error": "Missing required parameter: user_id"}), 400
            
        records = get_user_food_records(user_id, start_date, end_date, mealtime)
        return jsonify(records), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@food_bp.route('/record/<int:record_id>', methods=['DELETE'])
def remove_food_record(record_id):
    """
    刪除食物記錄
    ---
    查詢參數:
      user_id: 用戶ID (用於驗證權限)
    回應:
      200: 刪除成功
    """
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({"error": "Missing required parameter: user_id"}), 400
            
        result = delete_food_record(user_id, record_id)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@food_bp.route('/favorites', methods=['GET'])
def get_favorites():
    """
    獲取用戶收藏的食物清單
    ---
    查詢參數:
      user_id: 用戶ID
    回應:
      200: 收藏清單
    """
    try:
        user_id = request.args.get('user_id')
        
        if not user_id:
            return jsonify({"error": "Missing required parameter: user_id"}), 400
            
        favorites = get_user_favorites(user_id)
        return jsonify(favorites), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@food_bp.route('/favorites', methods=['POST'])
def add_favorite():
    """
    添加食物到收藏
    ---
    請求參數:
      user_id: 用戶ID
      food_id: 食物ID
    回應:
      201: 添加成功
    """
    try:
        data = request.json
        
        if 'user_id' not in data or 'food_id' not in data:
            return jsonify({"error": "Missing required fields: user_id and food_id"}), 400
            
        result = add_to_favorites(data['user_id'], data['food_id'])
        return jsonify(result), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@food_bp.route('/favorites', methods=['DELETE'])
def remove_favorite():
    """
    從收藏中移除食物
    ---
    請求參數:
      user_id: 用戶ID
      food_id: 食物ID
    回應:
      200: 移除成功
    """
    try:
        data = request.json
        
        if 'user_id' not in data or 'food_id' not in data:
            return jsonify({"error": "Missing required fields: user_id and food_id"}), 400
            
        result = remove_from_favorites(data['user_id'], data['food_id'])
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@food_bp.route('/exercise/calculator', methods=['GET'])
def calculate_exercise():
    """
    計算消耗卡路里需要的運動量
    ---
    查詢參數:
      calories: 要消耗的卡路里
    回應:
      200: 運動量建議
    """
    try:
        calories = request.args.get('calories')
        
        if not calories:
            return jsonify({"error": "Missing required parameter: calories"}), 400
            
        calories = float(calories)
        
        # 簡易的運動消耗計算
        exercises = [
            {
                "type": "跑步",
                "duration": round(calories / 10),  # 假設跑步消耗10大卡/分鐘
                "met": 10
            },
            {
                "type": "游泳",
                "duration": round(calories / 8),  # 假設游泳消耗8大卡/分鐘
                "met": 8
            },
            {
                "type": "騎腳踏車",
                "duration": round(calories / 7),  # 假設騎車消耗7大卡/分鐘
                "met": 7
            },
            {
                "type": "健走",
                "duration": round(calories / 5),  # 假設健走消耗5大卡/分鐘
                "met": 5
            }
        ]
        
        return jsonify({
            "calories": calories,
            "exercises": exercises
        }), 200
    except ValueError:
        return jsonify({"error": "Invalid calories value"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@food_bp.route('/record/<int:record_id>', methods=['PUT'])
def update_food_record(record_id):
    """
    修改食物記錄
    ---
    路徑參數:
      record_id: 食物記錄ID
    請求參數:
      user_id: 用戶ID (驗證權限)
      mealtime: 餐點類型 (可選)
      quantity: 數量 (可選)
      date: 日期 (可選)
    回應:
      200: 修改成功
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        if not user_id:
            return jsonify({"error": "Missing required field: user_id"}), 400
        # 允許部分欄位更新
        updates = {}
        for field in ['mealtime', 'quantity', 'date']:
            if field in data:
                updates[field] = data[field]
        if not updates:
            return jsonify({"error": "No fields to update"}), 400
        result = update_food_record_service(user_id, record_id, updates)
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500 