# 速Per Idol - 健康管理網站

速Per Idol 是一個全方位的健康飲食追蹤應用程式，幫助用戶管理日常飲食和營養攝取，促進健康生活方式。

## 專案架構

本專案採用前後端分離的架構：

### 前端技術棧

- **框架**: Vue 3 + Pinia (狀態管理)
- **路由**: Vue Router
- **UI組件**: Element Plus
- **HTTP客戶端**: Axios
- **構建工具**: Vite
- **代碼規範**: ESLint + Prettier

### 後端技術棧

- **框架**: Flask (Python)
- **數據庫**: MySQL
- **認證**: JWT
- **ORM**: SQLAlchemy (可選)

## 系統功能

1. **用戶認證與個人資料**
   - 註冊/登入
   - 個人健康信息設置
   - 飲食偏好設定

2. **食物記錄與搜索**
   - 食物數據庫搜索
   - 食物營養成分查詢
   - 每日飲食記錄

3. **運動記錄**
   - 運動活動記錄
   - 卡路里消耗計算
   - 運動建議

4. **數據分析與報告**
   - 週報告生成
   - 營養攝入分析
   - 卡路里消耗/攝入平衡
   - 進度追蹤

## 開發環境設置 (2025-0508更新)

### 前置需求
1. **Git** - 用於克隆專案
2. **Node.js** (建議版本 ≥ 18.0.0) 和 **npm** (建議版本 ≥ 8.0.0)
3. **Python** (建議版本 3.9+ 或 3.10+)
4. **MySQL** 數據庫 (遠程數據庫已配置，本地可以直接連接)

### 快速設置 (推薦)

我們提供了自動設置腳本，可以一鍵配置開發環境：

**Windows 用戶**:
```bash
cd super-idol/scripts
setup_dev.bat
```

**macOS/Linux 用戶**:
```bash
cd super-idol/scripts
chmod +x setup_dev.sh
./setup_dev.sh
```

這些腳本會自動完成以下步驟：
1. 創建必要的目錄結構
2. 設置環境變數文件 (.env)
3. 安裝前端和後端依賴
4. 構建前端並複製到後端靜態目錄

### 啟動開發環境 (三種方法)

#### 方法1: 同時運行前後端（推薦開發使用）

使用兩個終端分別運行前端和後端：

**終端1 (後端)**:
```bash
cd super-idol/backend
python run.py
```

**終端2 (前端)**:
```bash
cd super-idol/frontend
npm run dev
```

這是最可靠的方法，因為你可以單獨查看每個服務的日誌輸出，並在需要時單獨重啟任一服務。

#### 方法2: 使用整合腳本

```bash
cd super-idol/frontend
npm run dev:all
```

這個命令使用我們提供的腳本同時啟動前端和後端服務。

#### 方法3: 直接使用Node.js運行腳本

```bash
cd super-idol
node scripts/dev.js
```

### 訪問應用

- 前端: http://localhost:5173
- 後端 API: http://localhost:5000
- API測試端點: http://localhost:5000/api/test-cors

### 手動設置 (詳細步驟)

如果自動腳本不適合您的環境，以下是手動設置步驟：

1. **克隆專案**
   ```bash
   git clone <repository-url>
   cd super-idol
   ```

2. **安裝前端依賴**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

3. **安裝後端 Python 依賴**
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

4. **設置 MySQL 數據庫**
   - 默認配置已經設置使用遠程數據庫
   - 數據庫信息：
     - 主機: superidol.c9i82eygu8mk.ap-southeast-2.rds.amazonaws.com
     - 端口: 3306
     - 用戶名: DBMS11302
     - 密碼: ilovedbms
     - 數據庫名: superidol

5. **配置後端環境變數**
   - 在 `backend` 目錄中創建 `.env` 文件，填入以下內容：
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

6. **構建前端並複製到後端靜態目錄（可選，僅在需要生產模式下測試時）**
   ```bash
   cd frontend
   npm run build
   mkdir -p ../backend/static
   cp -r dist/* ../backend/static/
   cd ..
   ```

## 可能遇到的問題及解決方案

1. **CORS 跨域問題**
   - 問題表現: 在前端控制台看到 "Access to fetch at... has been blocked by CORS policy" 錯誤
   - 解決方案: 
     - 確保後端已正確啟動並在 http://localhost:5000 運行
     - 確保 `backend/app/__init__.py` 中的 CORS 設置正確
     - 如問題持續，可以使用瀏覽器的 CORS 插件臨時禁用 CORS
   
2. **前端API連接問題**
   - 問題表現: "API 連接失敗，請檢查後端是否運行" 或 "Network Error"
   - 解決方案:
     - 確認後端服務是否正在運行 (`python run.py`)
     - 訪問 http://localhost:5000/api/test-cors 測試API是否可用
     - 檢查前端的 API 基礎URL設置 (`frontend/src/services/api.js`)

3. **前端構建失敗 - 找不到 API 模塊**
   - 確認 `frontend/src/services/api.js` 文件存在
   - 確保文件末尾有 `export default api;` 語句

4. **找不到靜態文件**
   - 確保前端已構建 (`npm run build`) 
   - 確保 `backend/static` 目錄包含前端構建文件

5. **數據庫連接問題**
   - 確保網絡能夠連接到遠程數據庫
   - 檢查 `.env` 文件中的連接信息是否正確

6. **端口被佔用**
   - 如果 5173 或 5000 端口被佔用，可修改：
     - 前端: 在 `frontend/vite.config.js` 中調整端口
     - 後端: 在 `.env` 文件中添加 `PORT=其他端口號`

## 項目結構

```
super-idol/
├── frontend/              # 前端Vue項目
│   ├── src/
│   │   ├── assets/        # 靜態資源
│   │   ├── components/    # 共用元件
│   │   ├── pages/         # 頁面元件
│   │   ├── router/        # 路由配置
│   │   ├── services/      # API服務
│   │   ├── store/         # Pinia狀態
│   │   ├── utils/         # 工具函數
│   │   ├── App.vue        # 根組件
│   │   └── main.js        # 入口文件
│   └── ...
├── backend/               # 後端Flask項目
│   ├── app/
│   │   ├── api/           # API路由
│   │   ├── services/      # 業務邏輯
│   │   ├── utils/         # 工具函數
│   │   └── ...
│   ├── static/            # 靜態文件目錄(由前端構建生成)
│   └── ...
├── scripts/               # 腳本目錄
│   ├── dev.js             # 開發環境啟動腳本
│   ├── setup.js           # 環境設置腳本
│   ├── deploy.sh          # 部署腳本
│   └── ...
└── ...
```

## 前後端接口說明

### 認證接口

1. **註冊** 
   - 路徑: `/api/auth/signup`
   - 方法: POST
   - 請求體: `{ "name": "用戶名", "email": "用戶郵箱", "password": "密碼" }`
   - 響應: `{ "access_token": "JWT令牌", "user": { 用戶信息 } }`

2. **登入**
   - 路徑: `/api/auth/login`
   - 方法: POST
   - 請求體: `{ "email": "用戶郵箱", "password": "密碼" }`
   - 響應: `{ "access_token": "JWT令牌", "user": { 用戶信息 } }`

### 飲食記錄接口

1. **獲取食物列表**
   - 路徑: `/api/food`
   - 方法: GET
   - 請求頭: `Authorization: Bearer <access_token>`
   - 響應: `{ "foods": [ 食物列表 ] }`

2. **添加食物記錄**
   - 路徑: `/api/food`
   - 方法: POST
   - 請求頭: `Authorization: Bearer <access_token>`
   - 請求體: `{ "name": "食物名稱", "calories": 卡路里, "date": "YYYY-MM-DD", ... }`
   - 響應: `{ "id": 記錄ID, "message": "成功訊息" }`

### 運動記錄接口

1. **獲取運動列表**
   - 路徑: `/api/exercise`
   - 方法: GET
   - 請求頭: `Authorization: Bearer <access_token>`
   - 響應: `{ "exercises": [ 運動列表 ] }`

2. **添加運動記錄**
   - 路徑: `/api/exercise`
   - 方法: POST
   - 請求頭: `Authorization: Bearer <access_token>`
   - 請求體: `{ "name": "運動名稱", "calories": 消耗卡路里, "duration": 時長, ... }`
   - 響應: `{ "id": 記錄ID, "message": "成功訊息" }`

## 生產環境部署

本專案已配置為可在 Render.com 上部署：

1. 在 Render 上創建一個 Web Service
2. 連接到 GitHub 倉庫
3. 使用以下設置:
   - 構建命令: 參考 `render.yaml` 中的設置
   - 啟動命令: 參考 `render.yaml` 中的設置
   - 環境變數: 參考 `render.yaml` 中的設置

## 貢獻指南

1. Fork 此儲存庫
2. 創建您的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m '添加一些驚人的功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 開啟一個Pull Request

## 授權協議

本項目使用 [ISC 授權](LICENSE)。 