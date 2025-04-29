// 初始化圖表
function initChart() {
    const ctx = document.getElementById('nutrition-chart').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['週一', '週二', '週三', '週四', '週五', '週六', '週日'],
            datasets: [
                {
                    label: '熱量 (kcal)',
                    data: [2100, 2200, 2000, 2300, 2100, 2400, 2000],
                    borderColor: '#4CAF50',
                    tension: 0.1
                },
                {
                    label: '蛋白質 (g)',
                    data: [80, 85, 75, 90, 85, 95, 80],
                    borderColor: '#2196F3',
                    tension: 0.1
                },
                {
                    label: '碳水化合物 (g)',
                    data: [250, 260, 240, 270, 250, 280, 240],
                    borderColor: '#FFC107',
                    tension: 0.1
                },
                {
                    label: '脂肪 (g)',
                    data: [70, 75, 65, 80, 70, 85, 65],
                    borderColor: '#F44336',
                    tension: 0.1
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: '每週營養攝取趨勢'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

// 載入每日記錄
function loadDailyRecords() {
    const records = [
        { date: '2024-03-18', calories: 2100, protein: 80, carbs: 250, fat: 70 },
        { date: '2024-03-19', calories: 2200, protein: 85, carbs: 260, fat: 75 },
        { date: '2024-03-20', calories: 2000, protein: 75, carbs: 240, fat: 65 },
        { date: '2024-03-21', calories: 2300, protein: 90, carbs: 270, fat: 80 },
        { date: '2024-03-22', calories: 2100, protein: 85, carbs: 250, fat: 70 },
        { date: '2024-03-23', calories: 2400, protein: 95, carbs: 280, fat: 85 },
        { date: '2024-03-24', calories: 2000, protein: 80, carbs: 240, fat: 65 }
    ];

    const tbody = document.getElementById('daily-records-body');
    tbody.innerHTML = '';

    records.forEach(record => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${record.date}</td>
            <td>${record.calories}</td>
            <td>${record.protein}</td>
            <td>${record.carbs}</td>
            <td>${record.fat}</td>
            <td>
                <button class="btn-view" onclick="viewDetails('${record.date}')">查看詳情</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// 查看詳情
function viewDetails(date) {
    // TODO: 實現查看詳情功能
    console.log(`查看 ${date} 的詳情`);
}

// 匯出 PDF
document.getElementById('export-pdf').addEventListener('click', () => {
    // TODO: 實現匯出 PDF 功能
    console.log('匯出 PDF');
});

// 匯出 CSV
document.getElementById('export-csv').addEventListener('click', () => {
    // TODO: 實現匯出 CSV 功能
    console.log('匯出 CSV');
});

// 切換週次
document.getElementById('prev-week').addEventListener('click', () => {
    // TODO: 實現切換到上週
    console.log('切換到上週');
});

document.getElementById('next-week').addEventListener('click', () => {
    // TODO: 實現切換到下週
    console.log('切換到下週');
});

// 頁面載入時初始化
document.addEventListener('DOMContentLoaded', () => {
    initChart();
    loadDailyRecords();
}); 