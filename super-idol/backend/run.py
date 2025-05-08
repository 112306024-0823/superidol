"""
Application entry point.
"""

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os
import logging
import glob
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 檢查靜態文件目錄
def check_static_directory():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(base_dir, 'static')
    
    logger.info(f"檢查靜態目錄: {static_dir}")
    
    if not os.path.exists(static_dir):
        logger.warning(f"靜態目錄不存在，嘗試創建: {static_dir}")
        try:
            os.makedirs(static_dir, exist_ok=True)
        except Exception as e:
            logger.error(f"創建靜態目錄失敗: {str(e)}")
            return False
    
    # 檢查index.html是否存在
    index_path = os.path.join(static_dir, 'index.html')
    if not os.path.exists(index_path):
        logger.error(f"找不到index.html: {index_path}")
        # 列出目錄內容以便調試
        try:
            files = glob.glob(os.path.join(static_dir, '*'))
            logger.info(f"靜態目錄內容: {files}")
        except Exception as e:
            logger.error(f"無法列出目錄內容: {str(e)}")
        return False
    
    logger.info(f"index.html找到: {index_path}")
    return True

# 創建Flask應用
static_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
logger.info(f"靜態目錄設置為: {static_folder}")
app = Flask(__name__, static_folder=static_folder)
CORS(app)

# 引入API路由
from app.api import auth_bp, food_bp, exercise_bp, report_bp

# 註冊所有藍圖
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(food_bp, url_prefix='/api/food')
app.register_blueprint(exercise_bp, url_prefix='/api/exercise')
app.register_blueprint(report_bp, url_prefix='/api/report')

# 檢查靜態目錄
static_ok = check_static_directory()

# 調試端點
@app.route('/api/debug/static-info')
def static_info():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(base_dir, 'static')
    
    try:
        files = glob.glob(os.path.join(static_dir, '*'))
        file_list = [os.path.basename(f) for f in files]
    except Exception as e:
        file_list = [f"錯誤: {str(e)}"]
    
    return jsonify({
        'static_directory': static_dir,
        'directory_exists': os.path.exists(static_dir),
        'files': file_list,
        'app_static_folder': app.static_folder
    })

# 前端路由處理
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    logger.info(f"請求路徑: {path}")
    
    if path.startswith('api/'):
        # API請求由Flask處理
        logger.info("API請求路徑，返回404")
        return app.response_class(status=404)
    
    if path and path != '' and not path.startswith('api'):
        # 嘗試從靜態文件夾提供文件
        logger.info(f"嘗試提供靜態文件: {path}")
        try:
            full_path = os.path.join(app.static_folder, path)
            logger.info(f"檢查文件是否存在: {full_path}")
            if os.path.exists(full_path) and os.path.isfile(full_path):
                return send_from_directory(app.static_folder, path)
            logger.warning(f"文件不存在: {full_path}")
        except Exception as e:
            logger.error(f"提供靜態文件出錯: {str(e)}")
    
    # 默認返回index.html
    logger.info("嘗試返回index.html")
    try:
        if static_ok:
            return send_from_directory(app.static_folder, 'index.html')
        else:
            return "錯誤: 靜態文件目錄檢查失敗，找不到index.html。請檢查部署日誌獲取更多信息。", 500
    except Exception as e:
        logger.error(f"提供index.html出錯: {str(e)}")
        return f"錯誤: 無法加載前端應用。詳細信息: {str(e)}", 500

# 提供備用首頁
@app.route('/app-status')
def app_status():
    return """
    <html>
    <head><title>Super Idol 應用狀態</title></head>
    <body>
        <h1>Super Idol API服務正在運行</h1>
        <p>API路由可用，但無法找到前端靜態文件。</p>
        <p>請檢查部署日誌或訪問 <a href="/api/debug/static-info">/api/debug/static-info</a> 獲取更多診斷信息。</p>
    </body>
    </html>
    """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 