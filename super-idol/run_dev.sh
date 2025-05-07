#!/bin/bash

echo "正在啟動 Super Idol 開發環境..."

# 啟動後端
echo "啟動後端 (Flask)..."
cd backend && python run.py &
BACKEND_PID=$!

# 啟動前端
echo "啟動前端 (Vue)..."
cd ../frontend && npm run dev &
FRONTEND_PID=$!

echo "開發環境已啟動！"
echo "前端: http://localhost:5173"
echo "後端: http://localhost:5000"

# 捕獲中斷信號，清理進程
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait 