# 麥當勞台灣菜單與營養資訊爬蟲

## 功能
- 自動抓取麥當勞台灣官網所有菜單品項（名稱、圖片、分類、價格）
- 自動抓取營養資訊（熱量、蛋白質、脂肪、碳水等）
- 自動合併並輸出成 `mcdonalds_menu_with_nutrition.csv`

## 使用方式

1. 安裝 Python 3.8 以上
2. 安裝依賴：
   ```bash
   pip install -r requirements.txt
   ```
3. 執行爬蟲：
   ```bash
   python mcdonalds_crawler.py
   ```
4. 產出檔案：
   - `mcdonalds_menu_with_nutrition.csv`（UTF-8編碼，含所有欄位）

## 注意事項
- 官網結構若有變動，請用 Chrome F12 檢查 class 名稱並調整程式
- 若遇到連線問題可多重試幾次
- 僅供學術/專題/非商業用途，請勿用於商業營利
- 若需批量下載圖片，可再擴充腳本

## 欄位說明
- name：品項名稱
- category：分類
- image_url：圖片網址
- price：價格（如有）
- 其餘為營養資訊表格欄位 