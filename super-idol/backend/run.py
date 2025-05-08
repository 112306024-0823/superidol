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
    # 修改為使用前端構建目錄
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 上一級目錄(super-idol)
    static_dir = os.path.join(base_dir, 'frontend', 'dist')
    
    logger.info(f"檢查前端構建目錄: {static_dir}")
    
    if not os.path.exists(static_dir):
        logger.warning(f"前端構建目錄不存在，嘗試使用備用路徑")
        # 備用路徑 - backend/static
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        
        if not os.path.exists(static_dir):
            logger.warning(f"備用靜態目錄不存在，嘗試創建: {static_dir}")
            try:
                os.makedirs(static_dir, exist_ok=True)
                # 創建一個簡單的測試頁面
                index_html = os.path.join(static_dir, 'index.html')
                with open(index_html, 'w') as f:
                    f.write('<html><body><h1>Super Idol 測試頁面</h1><p>這是一個測試頁面，表示靜態文件服務正常工作，但找不到實際的前端構建文件。</p></body></html>')
                logger.info(f"已創建測試頁面: {index_html}")
            except Exception as e:
                logger.error(f"創建靜態目錄失敗: {str(e)}")
                return False, static_dir
    
    # 檢查index.html是否存在
    index_path = os.path.join(static_dir, 'index.html')
    if not os.path.exists(index_path):
        logger.error(f"找不到index.html: {index_path}")
        # 列出目錄內容以便調試
        try:
            files = glob.glob(os.path.join(static_dir, '*'))
            logger.info(f"目錄內容: {files}")
        except Exception as e:
            logger.error(f"無法列出目錄內容: {str(e)}")
        return False, static_dir
    
    logger.info(f"index.html找到: {index_path}")
    return True, static_dir

# 創建Flask應用
from app import create_app

# 獲取應用實例
app = create_app()

# 設置靜態文件目錄 - 使用檢查函數返回的路徑
static_ok, static_folder = check_static_directory()
app.static_folder = static_folder
logger.info(f"靜態目錄設置為: {static_folder}")

# 調試端點
@app.route('/api/debug/static-info')
def static_info():
    try:
        files = glob.glob(os.path.join(app.static_folder, '*'))
        file_list = [os.path.basename(f) for f in files]
    except Exception as e:
        file_list = [f"錯誤: {str(e)}"]
    
    # 安全過濾環境變數
    env_vars = {}
    for k, v in os.environ.items():
        if 'secret' not in k.lower() and 'password' not in k.lower() and 'key' not in k.lower():
            env_vars[k] = v
    
    return jsonify({
        'static_directory': app.static_folder,
        'directory_exists': os.path.exists(app.static_folder),
        'files': file_list,
        'static_check_result': static_ok,
        'environment': os.getenv('FLASK_ENV', 'development'),
        'database_host': app.config.get('MYSQL_HOST', 'not_set'),
        'safe_environment_variables': env_vars
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
    logger.info(f"嘗試返回index.html，從目錄: {app.static_folder}")
    try:
        return send_from_directory(app.static_folder, 'index.html')
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