import { initHeader } from './components/header.js';
import { initFooter } from './components/footer.js';
import { initFoodCard } from './components/food-card.js';
import { setupRouter } from './utils/router.js';

// Initialize components
document.addEventListener('DOMContentLoaded', () => {
    initHeader();
    initFooter();
    initFoodCard();
});

// Initialize page-specific scripts
const initializeComponents = () => {
    const currentPath = window.location.pathname;

    // Load page-specific scripts
    if (currentPath.startsWith('/dashboard/')) {
        import('./pages/dashboard.js');
    } else if (currentPath.startsWith('/food/')) {
        import('./pages/food.js');
    } else if (currentPath.startsWith('/reports/')) {
        import('./pages/reports.js');
    }
};

// Handle errors globally
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

// Handle unhandled promise rejections
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
});

// Handle network status
window.addEventListener('online', () => {
    console.log('Application is online');
});

window.addEventListener('offline', () => {
    console.log('Application is offline');
});

// 初始化路由
setupRouter();

// 載入頁面內容
async function loadPage() {
    const path = window.location.pathname;
    const app = document.getElementById('app');
    
    try {
        // 根據路徑載入對應的頁面
        if (path === '/reports/weekly') {
            const response = await fetch('/pages/reports/weekly.html');
            const html = await response.text();
            app.innerHTML = html;
        } else {
            // 預設載入首頁
            app.innerHTML = '<h1>歡迎使用 Super Idol</h1>';
        }
    } catch (error) {
        console.error('載入頁面失敗:', error);
        app.innerHTML = '<h1>頁面載入失敗</h1>';
    }
}

// 監聽路由變化
window.addEventListener('popstate', loadPage);

// 初始載入
loadPage(); 