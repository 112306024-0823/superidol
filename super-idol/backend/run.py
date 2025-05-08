"""
Application entry point.
"""

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
import os
import logging
import glob
import shutil
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 尋找靜態文件目錄
def find_static_directory():
    """尋找最佳的靜態文件目錄，按優先級：
    1. ./static (直接在當前目錄下的靜態目錄)
    2. ../frontend/dist (前端構建目錄)
    3. 各種可能的 Render 環境下的絕對路徑
    """
    # 獲取當前文件目錄
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    # 上一級目錄，即super-idol目錄
    project_dir = os.path.dirname(backend_dir)
    
    # 記錄當前檔案和目錄資訊
    logger.info(f"當前檔案路徑: {__file__}")
    logger.info(f"後端目錄: {backend_dir}")
    logger.info(f"項目目錄: {project_dir}")
    logger.info(f"工作目錄: {os.getcwd()}")
    
    # 嘗試可能的靜態目錄路徑，按優先級順序
    possible_paths = [
        os.path.join(backend_dir, 'static'),           # 後端靜態目錄
        os.path.join(project_dir, 'frontend', 'dist'),  # 前端構建目錄
    ]
    
    # 嘗試各種可能的 Render 路徑
    render_base_paths = [
        '/opt/render/project/src',             # 基本 Render 路徑
        '/opt/render/project'                  # 備用 Render 路徑
    ]
    
    # 嘗試可能的專案結構
    project_structures = [
        ['backend', 'static'],                 # /backend/static
        ['super-idol', 'backend', 'static'],   # /super-idol/backend/static
        ['frontend', 'dist'],                  # /frontend/dist
        ['super-idol', 'frontend', 'dist']     # /super-idol/frontend/dist
    ]
    
    # 為 Render 環境添加所有可能的絕對路徑
    if os.environ.get('RENDER') == 'true':
        render_paths = []
        for base_path in render_base_paths:
            for structure in project_structures:
                path = os.path.join(base_path, *structure)
                render_paths.append(path)
        # 在最高優先級添加這些路徑
        possible_paths = render_paths + possible_paths
    
    # 記錄所有要檢查的路徑
    logger.info(f"將檢查以下路徑: {possible_paths}")
    
    found_path = None
    
    # 檢查每個可能的路徑
    for path in possible_paths:
        logger.info(f"檢查靜態目錄: {path}")
        
        if os.path.exists(path):
            logger.info(f"目錄存在: {path}")
            # 檢查index.html是否存在
            index_path = os.path.join(path, 'index.html')
            if os.path.exists(index_path) and os.path.isfile(index_path):
                logger.info(f"找到有效的靜態目錄: {path}")
                found_path = path
                break
            else:
                try:
                    # 檢查目錄內有哪些文件
                    files = os.listdir(path)
                    logger.warning(f"目錄存在但沒有index.html: {path}，內容: {files}")
                except Exception as e:
                    logger.warning(f"讀取目錄內容失敗: {path}, 錯誤: {str(e)}")
        else:
            logger.warning(f"目錄不存在: {path}")
    
    # 如果找不到任何有效目錄，使用後端靜態目錄並創建簡單的index.html
    if not found_path:
        static_dir = os.path.join(backend_dir, 'static')
        logger.warning(f"未找到任何有效靜態目錄，將使用並創建: {static_dir}")
        
        try:
            os.makedirs(static_dir, exist_ok=True)
            index_html = os.path.join(static_dir, 'index.html')
            
            # 創建簡單的測試頁面
            with open(index_html, 'w') as f:
                f.write('''
                <!DOCTYPE html>
                <html lang="zh-TW">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Super Idol 測試頁面</title>
                    <style>
                        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
                        h1 { color: #333; }
                        .error { color: #e74c3c; }
                        .info { color: #3498db; }
                    </style>
                </head>
                <body>
                    <h1>Super Idol 應用啟動成功</h1>
                    <p class="info">API 服務正常運行，但找不到前端文件。</p>
                    <p>可能的原因:</p>
                    <ul>
                        <li>前端尚未構建</li>
                        <li>前端構建文件未複製到靜態目錄</li>
                        <li>靜態文件路徑配置有誤</li>
                    </ul>
                    <p>請檢查部署日誌或訪問 <a href="/api/debug/static-info">/api/debug/static-info</a> 獲取更多信息。</p>
                </body>
                </html>
                ''')
            
            logger.info(f"成功創建測試頁面: {index_html}")
            found_path = static_dir
        except Exception as e:
            logger.error(f"創建靜態目錄或測試頁面失敗: {str(e)}")
            return None
    
    # 嘗試複製前端文件到後端靜態目錄(如果需要)
    if found_path == os.path.join(project_dir, 'frontend', 'dist'):
        static_dir = os.path.join(backend_dir, 'static')
        try:
            # 確保後端靜態目錄存在
            os.makedirs(static_dir, exist_ok=True)
            
            # 只在後端靜態目錄不包含index.html時進行複製
            if not os.path.exists(os.path.join(static_dir, 'index.html')):
                logger.info(f"複製前端文件到後端靜態目錄: {found_path} -> {static_dir}")
                
                # 清理目標目錄
                for item in os.listdir(static_dir):
                    item_path = os.path.join(static_dir, item)
                    try:
                        if os.path.isfile(item_path):
                            os.unlink(item_path)
                        elif os.path.isdir(item_path):
                            shutil.rmtree(item_path)
                    except Exception as e:
                        logger.warning(f"清理文件失敗: {item_path}, 錯誤: {str(e)}")
                
                # 複製文件
                for item in os.listdir(found_path):
                    s = os.path.join(found_path, item)
                    d = os.path.join(static_dir, item)
                    if os.path.isfile(s):
                        shutil.copy2(s, d)
                    else:
                        shutil.copytree(s, d)
                
                logger.info(f"複製完成，後端靜態目錄現在包含: {os.listdir(static_dir)}")
                found_path = static_dir
        except Exception as e:
            logger.error(f"複製前端文件到後端靜態目錄失敗: {str(e)}")
            # 繼續使用前端目錄
    
    return found_path

# 創建Flask應用
from app import create_app

# 獲取應用實例
app = create_app()

# 設置靜態文件目錄
static_folder = find_static_directory()
if static_folder:
    app.static_folder = static_folder
    logger.info(f"設置靜態目錄為: {static_folder}")
else:
    logger.error("無法找到或創建有效的靜態文件目錄！")

# 調試端點
@app.route('/api/debug/static-info')
def static_info():
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(backend_dir)
    
    # 檢查可能的靜態目錄
    paths_info = {}
    for path in [
        os.path.join(project_dir, 'frontend', 'dist'),
        os.path.join(backend_dir, 'static')
    ]:
        try:
            exists = os.path.exists(path)
            files = []
            if exists:
                files = [os.path.basename(f) for f in glob.glob(os.path.join(path, '*'))]
            paths_info[path] = {
                'exists': exists,
                'files': files,
                'has_index_html': 'index.html' in files
            }
        except Exception as e:
            paths_info[path] = {'error': str(e)}
    
    # 安全過濾環境變數
    env_vars = {}
    for k, v in os.environ.items():
        if not any(s in k.lower() for s in ['secret', 'password', 'key']):
            env_vars[k] = v
    
    return jsonify({
        'app_static_folder': app.static_folder,
        'static_paths': paths_info,
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
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(backend_dir)
    
    # 檢查各種路徑
    paths = [
        ('前端構建目錄', os.path.join(project_dir, 'frontend', 'dist')),
        ('後端靜態目錄', os.path.join(backend_dir, 'static')),
        ('Flask 靜態目錄', app.static_folder)
    ]
    
    path_info = []
    for name, path in paths:
        exists = os.path.exists(path)
        has_index = exists and os.path.exists(os.path.join(path, 'index.html'))
        path_info.append(f"{name}: {path} (存在: {exists}, 包含index.html: {has_index})")
    
    return f"""
    <html>
    <head>
        <title>Super Idol 應用狀態</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
            h1 {{ color: #333; }}
            pre {{ background: #f5f5f5; padding: 10px; border-radius: 5px; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <h1>Super Idol API服務正在運行</h1>
        <p>API路由可用，但前端靜態文件可能有問題。</p>
        <h2>路徑信息:</h2>
        <pre>{chr(10).join(path_info)}</pre>
        <p>詳細診斷: <a href="/api/debug/static-info">/api/debug/static-info</a></p>
    </body>
    </html>
    """

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 