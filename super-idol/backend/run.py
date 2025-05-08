"""
Application entry point.
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
import os
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 創建Flask應用
app = Flask(__name__, static_folder='static')
CORS(app)

# 引入API路由
from app.api import auth_bp, food_bp, exercise_bp, report_bp

# 註冊所有藍圖
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(food_bp, url_prefix='/api/food')
app.register_blueprint(exercise_bp, url_prefix='/api/exercise')
app.register_blueprint(report_bp, url_prefix='/api/report')

# 前端路由處理
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path.startswith('api/'):
        # API請求由Flask處理
        return app.response_class(status=404)
    
    if path and path != '' and not path.startswith('api'):
        # 嘗試從靜態文件夾提供文件
        try:
            return send_from_directory(app.static_folder, path)
        except:
            pass
    # 默認返回index.html
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 