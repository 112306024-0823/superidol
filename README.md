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

## 開發環境設置

### 前置需求
1. **Git** - 用於克隆專案
2. **Node.js** (建議版本 ≥ 18.0.0) 和 **npm** (建議版本 ≥ 8.0.0)
3. **Python** (建議版本 3.9+ 或 3.10+)
4. **MySQL** 數據庫

### 詳細安裝步驟

1. **克隆專案**
   ```bash
   git clone https://github.com/your-username/super-idol.git
   cd super-idol
   ```

2. **安裝所有依賴**
   ```bash
   npm run install-all
   ```
   這將自動安裝根目錄和前端目錄的 Node.js 依賴。

3. **安裝後端 Python 依賴**
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

4. **設置 MySQL 數據庫**
   - 確保您已安裝並啟動 MySQL 服務
   - 創建新的數據庫用於此專案
   - **注意**: 如果團隊成員需要連接到相同的數據庫，請向項目管理員或數據庫管理員索取正確的連接資訊

5. **配置後端環境變數**
   - 在 `backend` 目錄中創建 `.env` 文件
   - **注意**: `.env` 文件不包含在版本控制中，您需要手動創建
   - 如果您需要連接到團隊共享的數據庫，請向項目管理員獲取正確的環境變數設定
   - 或使用以下模板創建您自己的本地配置:
     ```
     DB_USER=你的數據庫用戶名
     DB_PASSWORD=你的數據庫密碼
     DB_HOST=localhost
     DB_PORT=3306
     DB_NAME=super_idol_db
     JWT_SECRET_KEY=your_secret_key_here
     ```
   - 您也可以在 `backend` 目錄中創建一個名為 `.env.example` 的文件，包含如下內容供未來開發者參考:
     ```
     # 數據庫配置
     DB_USER=database_username
     DB_PASSWORD=database_password
     DB_HOST=localhost
     DB_PORT=3306
     DB_NAME=super_idol_db
     
     # JWT認證配置
     JWT_SECRET_KEY=your_secret_key_here
     
     # 可選: 調整應用設置
     # FLASK_ENV=development
     # FLASK_APP=run.py
     # PORT=5000
     ```

6. **啟動開發環境**
   - 使用 Windows：
     ```bash
     run_dev.bat
     ```
     **注意**: 執行此批處理檔案會自動同時啟動前端和後端服務，無需其他操作
   - 使用 macOS/Linux：
     ```bash
     ./run_dev.sh
     ```
   - 或使用 npm 腳本同時啟動前後端：
     ```bash
     npm run dev
     ```

7. **訪問應用**
   - 前端: http://localhost:5173
   - 後端 API: http://localhost:5000

### 可能遇到的問題及解決方案

1. **MySQL 連接問題**
   - 確保 MySQL 服務已啟動
   - 確認用戶名和密碼正確
   - 檢查數據庫是否已創建

2. **Python 依賴安裝問題**
   - 可以嘗試使用虛擬環境：
     ```bash
     python -m venv venv
     # Windows
     venv\Scripts\activate
     # macOS/Linux
     source venv/bin/activate
     pip install -r requirements.txt
     ```

3. **端口被佔用**
   - 如果 5173 或 5000 端口被佔用，可修改：
     - 前端: 在 `frontend/vite.config.js` 中調整端口
     - 後端: 在 `backend/run.py` 中調整端口

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
│   ├── scripts/           # 數據庫腳本等
│   └── ...
├── run_dev.sh             # 開發環境啟動腳本 (Unix)
├── run_dev.bat            # 開發環境啟動腳本 (Windows)
└── ...
```

## 生產環境部署

1. 構建前端應用
   ```bash
   npm run build
   ```

2. 配置後端服務器
   設置適當的生產環境變數，並根據需要調整Flask配置。

3. 使用適當的Web服務器（如Nginx）和WSGI服務器（如Gunicorn）部署後端。

## 貢獻指南

1. Fork 此儲存庫
2. 創建您的功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m '添加一些驚人的功能'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 開啟一個Pull Request

## 授權協議

本項目使用 [ISC 授權](LICENSE)。