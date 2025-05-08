"""
Application entry point.
"""

from flask import Flask, send_from_directory
from flask_cors import CORS
import os
import logging
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 創建Flask應用
static_folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
logger.info(f"靜態目錄路徑: {static_folder_path}")
app = Flask(__name__, static_folder=static_folder_path)
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
    logger.info(f"請求路徑: {path}")
    
    if path.startswith('api/'):
        # API請求由Flask處理
        logger.info("API請求，返回404")
        return app.response_class(status=404)
    
    if path and path != '' and not path.startswith('api'):
        # 嘗試從靜態文件夾提供文件
        logger.info(f"嘗試提供靜態文件: {path}")
        try:
            return send_from_directory(app.static_folder, path)
        except Exception as e:
            logger.error(f"提供靜態文件出錯: {str(e)}")
            pass
    
    # 默認返回index.html
    logger.info("返回index.html")
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except Exception as e:
        logger.error(f"提供index.html出錯: {str(e)}")
        return f"錯誤: 無法加載前端應用。詳細信息: {str(e)}", 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 