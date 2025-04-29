import { foodAPI } from '../utils/api.js';
import { Chart } from 'chart.js/auto';

export function initDashboard() {
    const chartContainer = document.querySelector('.chart-container');
    if (!chartContainer) return;

    // 獲取食物數據
    foodAPI.getFoods()
        .then(foods => {
            // 創建圖表
            const ctx = chartContainer.getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: foods.map(food => food.name),
                    datasets: [{
                        label: '卡路里',
                        data: foods.map(food => food.calories),
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => {
            console.error('Failed to load food data:', error);
        });
} 