# Super Idol 管理系統

這是一個用於管理偶像和投票的系統。

## 功能特點

- 用戶認證與授權
- 偶像信息管理
- 投票系統
- 數據統計與分析

## 技術棧

### 後端
- Flask
- SQLAlchemy
- JWT 認證
- RESTful API

### 前端
- Vite
- HTML/CSS/JavaScript
- 響應式設計

## 安裝與設置

1. 克隆專案
```bash
git clone https://github.com/your-username/super-idol.git
cd super-idol
```

2. 設置環境變量
```bash
cp .env.example .env
# 編輯 .env 文件，填入必要的配置
```

3. 設置後端
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

4. 設置前端
```bash
cd frontend
npm install
```

## 運行

1. 啟動後端
```bash
cd backend
python run.py
```

2. 啟動前端
```bash
cd frontend
npm run dev
```

## 測試

```bash
# 運行後端測試
cd backend
python -m pytest

# 運行前端測試
cd frontend
npm test
```

## 部署

使用 `scripts/deploy.sh` 腳本進行部署。

## 貢獻指南

1. Fork 專案
2. 創建特性分支
3. 提交更改
4. 推送到分支
5. 創建 Pull Request

## 許可證

MIT 