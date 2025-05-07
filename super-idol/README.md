1. System Overview | 系統概述

Pain Point | 痛點：
在追求健康體態與控制飲食的運動族群中，生活中對垃圾食物的需求仍然存在，如何在享受垃圾食物的同時保持健康的飲食紀律則成為一大挑戰。這導致消費者在選擇時常面臨以下困擾：
難以快速比較各種垃圾食物的熱量、營養價值與價格，導致選擇時猶豫與焦慮
缺乏對長期飲食選擇對健康與體態影響的視覺化回饋
缺少能夠結合運動與飲食紀錄、並提供回饋與鼓勵的整合性工具，難以持續維持動力


Proposed Solution | 解決方案：
本系統致力於成為用戶在速食、飲料、披薩選擇與健康管理上的全方位助理，提供以下功能：
垃圾食物資料整合與智慧搜尋：提供多家速食、飲料、披薩店的餐點熱量、營養、價格資訊，並支援依「店家」、「餐點」、「價格範圍」、「卡路里區間」等條件進行搜尋與篩選，幫助使用者快速找出符合需求的選項。
飲食消費紀錄與提醒：用戶可記錄每週的垃圾食物消費與攝取內容。針對「高熱量/低營養價值」的餐點進行消費紀錄與標記，根據消費者的飲食習慣做建議和提醒。
每週報告（Weekly Report）：每週統整使用者的垃圾食物總支出與攝取總卡路里。提供視覺化報表（如圓餅圖/長條圖）呈現熱量與費用占比。顯示「不健康飲食支出比例」，作為反思與改善的依據。
2. System Features | 系統功能
Calorie & Nutrient Database | 熱量與營養資料庫
User Profile & Dietary Preferences | 使用者個人檔案與飲食偏好
Weekly Data Analytics & Reporting | 每周數據分析與報告
Category
Function
Description
User Permissions
Register


使用者可以註冊帳號，建立個人資料（包含 User ID、名稱、Email、密碼、預算、每週熱量限制）


Login
使用者可以登入系統，存取個人化功能，如記錄餐點與支出


Edit Profile
使用者可以更新個人資料，如名稱、Email、預算、每週熱量限制等資訊
Food Records
Edit Meal
使用者可以修改已記錄的餐點資訊，如名稱、總熱量、價格等


Delete Meal
使用者可以刪除特定的餐點紀錄
Search Food
Food Filter
使用者能夠選擇價格、熱量區間、食物項目，來找到適合的餐點






Food Management
Add Food Item
使用者可以新增食物項目，包含名稱、單位、
單位熱量等資訊


Food Record
使用者可以將多個食物項目加入餐點，並設定數量，記錄在 Meal_FoodItem 關聯表


My Favorite
使用者可先將有興趣的餐點加入我的最愛
Week Report Management
View Weekly Report
檢視本週攝取與消耗的卡路里、總運動時間與不健康飲食支出


Analyze Trends
分析多週報告，幫助掌握飲食與運動狀況
Exercise Tracking
Log Exercise
紀錄運動項目、時間、卡路里消耗


Edit/Delete Exercise
修改或刪除特定的運動紀錄

3. ERD
主要實體 (Entities)
User (使用者)
    UserID (PK) - 使用者唯一識別碼
    Name - 使用者名稱
    Email - 電子郵件
    PasswordHash - 密碼（加密存儲）
    Budget - 預算
    WeekCalorieLimit - 每周熱量限制
Exercise_Preference
    Exercise_Name(PK) - 運動名稱
    UserID (FK) - 關聯使用者
Food_Preference
    FoodID(FK) - 食物ID
    UserID (FK) - 關聯使用者
    FoodID+UserID(PK)-複合主鍵
Restuarant_Preference
    Restuarant_ID(PK) - 食物名稱
    UserID (FK) - 關聯使用者

My_Favorite(我的最愛)
    FoodID(FK)
    UserID(FK)
_______________________________________________
Food(餐點)
    FoodID (PK) - 餐點唯一識別碼
    UserID (FK) - 關聯使用者
    Name - 餐點名稱
    Calories - 餐點總熱量
    Price - 餐點總花費
    Unit - 單位 (幾克/幾毫升)
    SetType - 紀錄是套餐 or 單點
    FoodType - 針對單點食物紀錄類型 (Burgers/ Snacks / Fried Chicken/ Pizza/ Beverages……)

Food_Record(紀錄使用者購買餐點)
    RecordID (PK) - Record項目唯一識別碼
    FoodID (FK) - 關聯食物
    UserID (FK) - 關聯使用者
    Date - 用餐日期
    MealTime- 用餐時段('breakfast', 'lunch', 'dinner', 'supper')

Restaurant
    RestaurantID (PK) - 餐廳唯一識別碼
    Type-餐廳類型
    Name - 餐廳名稱
    AveragePrice - 平均價格
_______________________________________________
Exercise_Record
    Exercise_Name (PK) - 運動名稱
    UserID (FK) - 關聯使用者
    Type - 運動類型（如跑步機、飛輪、游泳等）
    Duration - 運動時長
    CaloriesBurned - 所消耗的卡路里
    Date - 運動日期

Exercise Item(紀錄各種運動項目的基本資訊，看怎麼算User 消耗的卡路里，尚未確認)
    Exercise_Name(PK)- 運動名稱
    CaloriesConsumed - 攝取的卡路里
_______________________________________________
Week_Report( 不建表，直接用SQL寫邏輯 算資料)
    ReportID (PK) - 報告唯一識別碼
    UserID (FK) - 關聯使用者
    Exercise_Name (FK) - 運動名稱 
    RecordID(FK)
    Date - 該報告所涵蓋的日期
    TotalCaloriesConsumed - 總攝取的卡路里
    TotalCaloriesBurned - 運動消耗的總卡路里
    TotalExerciseDuration - 總運動時長
    UnhealthyExpense - 不健康飲食總支出