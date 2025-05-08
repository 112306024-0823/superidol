# Super Idol 健康管理網站

一個健康管理平台，幫助用戶追蹤健身進度、飲食計劃和健康數據。

## 技術堆疊

- **前端**: Vue.js (Vite)
- **後端**: Flask (Python)
- **資料庫**: MySQL
- **部署**: Render.com

## 本地安裝

### 前置需求

- Node.js 16+ 和 npm
- Python 3.8+
- MySQL

### 安裝步驟

#### Windows

1. 複製專案
```
git clone https://github.com/your-username/super-idol.git
cd super-idol
```

2. 執行自動安裝腳本
```
.\setup_dev.bat
```

3. 啟動開發伺服器
```
# 前端 (從super-idol根目錄)
cd frontend
npm run dev

# 後端 (從super-idol根目錄)
cd backend
python run.py
```

#### Linux/macOS

1. 複製專案
```
git clone https://github.com/your-username/super-idol.git
cd super-idol
```

2. 執行自動安裝腳本
```
chmod +x setup_dev.sh
./setup_dev.sh
```

3. 啟動開發伺服器
```
# 前端 (從super-idol根目錄)
cd frontend
npm run dev

# 後端 (從super-idol根目錄)
cd backend
python run.py
```

### 手動安裝

如果自動安裝腳本無法正常工作，你可以按照以下步驟手動安裝：

1. 設置前端
```
cd frontend
npm install
npm run build
```

2. 設置後端
```
cd backend
pip install -r requirements.txt
```

3. 創建環境變數檔案 `backend/.env`
```
DB_HOST=superidol.c9i82eygu8mk.ap-southeast-2.rds.amazonaws.com
DB_PORT=3306
DB_USER=DBMS11302
DB_PASSWORD=ilovedbms
DB_NAME=superidol
FLASK_ENV=development
JWT_SECRET_KEY=dev-key-for-local-development
SECRET_KEY=local-dev-secret-key
```

4. 複製前端構建到後端靜態目錄
```
mkdir -p backend/static
cp -r frontend/dist/* backend/static/
```

## 部署到 Render.com

### 使用 render.yaml 自動部署

1. Fork 這個專案到你的 GitHub 帳號
2. 在 Render.com 上創建一個新的 Web Service
3. 連接到你的 GitHub 倉庫
4. Render 將自動檢測 `render.yaml` 並設置服務

### 手動部署

1. 在 Render.com 創建一個新的 Web Service
2. 連接到你的 GitHub 倉庫
3. 使用以下設定:
   - **環境**: Python
   - **構建命令**:
     ```
     cd frontend && npm install && npm run build && 
     mkdir -p ../backend/static && 
     cp -r dist/* ../backend/static/ && 
     cd ../backend && 
     pip install -r requirements.txt
     ```
   - **啟動命令**:
     ```
     cd backend && gunicorn --bind 0.0.0.0:$PORT run:app
     ```
   - **環境變數**:
     ```
     DB_HOST=superidol.c9i82eygu8mk.ap-southeast-2.rds.amazonaws.com
     DB_PORT=3306
     DB_USER=DBMS11302
     DB_PASSWORD=ilovedbms
     DB_NAME=superidol
     FLASK_ENV=production
     JWT_SECRET_KEY=(生成一個安全的隨機值)
     SECRET_KEY=(生成一個安全的隨機值)
     ```

## 開發指南

### 目錄結構

```
super-idol/
├── frontend/         # Vue.js 前端
│   ├── src/          # 源碼
│   ├── public/       # 靜態文件
│   ├── dist/         # 構建輸出 (自動生成)
│   └── package.json  # 依賴和腳本
│
├── backend/          # Flask 後端
│   ├── app/          # 應用核心
│   ├── static/       # 靜態文件 (前端構建)
│   ├── run.py        # 入口點
│   └── requirements.txt # Python 依賴
│
├── setup_dev.bat     # Windows 安裝腳本
└── setup_dev.sh      # Linux/macOS 安裝腳本
```

### Git 分支策略

我們的團隊遵循以下分支命名規範：

- `main`: 生產環境分支
- `dev`: 開發環境分支
- `dev/frontend/[developer]`: 前端開發分支
- `dev/backend/[developer]`: 後端開發分支

### 開發工作流

1. 從 `dev` 分支創建個人開發分支
2. 在你的分支上進行開發
3. 提交 Pull Request 到 `dev` 分支
4. 代碼審查後合併
5. 定期將 `dev` 分支合併到 `main` 分支進行部署

## 故障排除

### 靜態文件無法載入

如果部署後無法正確加載前端頁面：

1. 確認前端構建成功（檢查 `frontend/dist` 目錄）
2. 確認靜態文件已複製到後端（檢查 `backend/static` 目錄）
3. 訪問 `/api/debug/static-info` 端點查看靜態文件目錄資訊
4. 檢查 Flask 日誌以獲取更多資訊 