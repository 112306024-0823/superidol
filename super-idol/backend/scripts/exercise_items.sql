-- 創建運動項目表（如果不存在）
CREATE TABLE IF NOT EXISTS ExerciseItem (
    Exercise_Name VARCHAR(50) PRIMARY KEY,
    MET DECIMAL(5,2) NOT NULL,
    Status ENUM('active', 'inactive') DEFAULT 'active'
);

-- 清空現有數據（可選）
-- TRUNCATE TABLE ExerciseItem;

-- 插入運動項目數據
INSERT IGNORE INTO ExerciseItem (Exercise_Name, MET) VALUES
('籃球', 7.0),
('快走', 4.0),
('騎腳踏車', 6.0),
('健走', 6.0),
('伏地挺身', 5.0),
('攀岩', 8.0),
('划船', 7.0),
('跑步(8km/hr)', 8.0),
('跑步(10km/hr)', 10.0),
('足球', 7.0),
('游泳', 7.0),
('打太極', 4.0),
('慢走', 3.0),
('瑜珈', 5.0);

-- 確認數據已插入
SELECT * FROM ExerciseItem; 