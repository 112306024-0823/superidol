/*
    檔案：exercise.js
    用途：運動頁面的互動功能
    功能：
    - 處理運動記錄表單提交
    - 更新運動統計數據
    - 顯示運動歷史記錄
*/

// DOM 元素
const exerciseForm = document.getElementById('exerciseForm');
const historyList = document.querySelector('.history-list');

// 運動記錄數據
let exerciseRecords = JSON.parse(localStorage.getItem('exerciseRecords')) || [];

// 初始化頁面
document.addEventListener('DOMContentLoaded', () => {
    // 頁面初始化邏輯將在這裡實現
    updateStats();
    displayHistory();
});

// 表單提交處理
exerciseForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const exerciseType = document.getElementById('exerciseType').value;
    const duration = parseInt(document.getElementById('duration').value);
    const calories = parseInt(document.getElementById('calories').value);

    // 創建新的運動記錄
    const newRecord = {
        id: Date.now(),
        type: exerciseType,
        duration: duration,
        calories: calories,
        date: new Date().toISOString()
    };

    // 添加到記錄列表
    exerciseRecords.push(newRecord);
    localStorage.setItem('exerciseRecords', JSON.stringify(exerciseRecords));

    // 更新顯示
    updateStats();
    displayHistory();

    // 重置表單
    exerciseForm.reset();
});

// 更新統計數據
function updateStats() {
    const today = new Date().toISOString().split('T')[0];
    const todayRecords = exerciseRecords.filter(record => 
        record.date.startsWith(today)
    );
    const thisWeekRecords = exerciseRecords.filter(record => {
        const recordDate = new Date(record.date);
        const today = new Date();
        const diffTime = Math.abs(today - recordDate);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
        return diffDays <= 7;
    });

    // 更新今日運動時間
    const todayDuration = todayRecords.reduce((sum, record) => sum + record.duration, 0);
    document.querySelector('.stat-card:nth-child(1) .stat-value').textContent = 
        `${todayDuration} 分鐘`;

    // 更新本週運動次數
    document.querySelector('.stat-card:nth-child(2) .stat-value').textContent = 
        `${thisWeekRecords.length} 次`;

    // 更新總消耗卡路里
    const totalCalories = exerciseRecords.reduce((sum, record) => sum + record.calories, 0);
    document.querySelector('.stat-card:nth-child(3) .stat-value').textContent = 
        `${totalCalories} kcal`;
}

// 顯示歷史記錄
function displayHistory() {
    historyList.innerHTML = '';

    if (exerciseRecords.length === 0) {
        historyList.innerHTML = '<p class="no-records">暫無運動記錄</p>';
        return;
    }

    // 按日期排序（最新的在前）
    const sortedRecords = [...exerciseRecords].sort((a, b) => 
        new Date(b.date) - new Date(a.date)
    );

    sortedRecords.forEach(record => {
        const recordElement = document.createElement('div');
        recordElement.className = 'history-item';
        recordElement.innerHTML = `
            <div class="record-info">
                <span class="record-type">${getExerciseTypeName(record.type)}</span>
                <span class="record-date">${formatDate(record.date)}</span>
            </div>
            <div class="record-details">
                <span>時間：${record.duration} 分鐘</span>
                <span>卡路里：${record.calories} kcal</span>
            </div>
        `;
        historyList.appendChild(recordElement);
    });
}

// 獲取運動類型的中文名稱
function getExerciseTypeName(type) {
    const typeNames = {
        'running': '跑步',
        'cycling': '騎自行車',
        'swimming': '游泳',
        'walking': '健走'
    };
    return typeNames[type] || type;
}

// 格式化日期
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('zh-TW', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
} 