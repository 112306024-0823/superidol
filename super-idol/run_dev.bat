@echo off
echo 正在啟動 Super Idol 開發環境...

echo 啟動後端 (Flask)...
start cmd /k "cd backend && python run.py"

echo 啟動前端 (Vue)...
start cmd /k "cd frontend && npm run dev"

echo 開發環境已啟動！
echo 前端: http://localhost:5173
echo 後端: http://localhost:5000 