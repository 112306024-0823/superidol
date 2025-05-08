@echo off
echo ===== 設置 Super Idol 本地開發環境 =====

echo 1. 檢查後端目錄...
if not exist backend\static mkdir backend\static
echo 後端靜態目錄確認: backend\static

echo 2. 創建後端環境變數文件...
echo DB_HOST=superidol.c9i82eygu8mk.ap-southeast-2.rds.amazonaws.com> backend\.env
echo DB_PORT=3306>> backend\.env
echo DB_USER=DBMS11302>> backend\.env
echo DB_PASSWORD=ilovedbms>> backend\.env
echo DB_NAME=superidol>> backend\.env
echo FLASK_ENV=development>> backend\.env
echo JWT_SECRET_KEY=dev-key-for-local-development>> backend\.env
echo SECRET_KEY=local-dev-secret-key>> backend\.env
echo 環境變數文件已創建: backend\.env

echo 3. 安裝前端依賴...
cd frontend
npm install
if %errorlevel% neq 0 (
    echo 錯誤: 前端依賴安裝失敗
    exit /b %errorlevel%
)
cd ..

echo 4. 安裝後端依賴...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo 錯誤: 後端依賴安裝失敗
    exit /b %errorlevel%
)
cd ..

echo 5. 構建前端並複製到後端靜態目錄...
cd frontend
npm run build
if %errorlevel% neq 0 (
    echo 錯誤: 前端構建失敗
    exit /b %errorlevel%
)
echo 複製前端文件到後端...
xcopy /E /Y dist\* ..\backend\static\
cd ..

echo ===== 設置完成 =====
echo.
echo 您現在可以運行 run_dev.bat 啟動應用
echo 或者使用 "npm run dev" 命令
echo.
echo 前端開發服務器: http://localhost:5173
echo 後端API服務器: http://localhost:5000
echo. 