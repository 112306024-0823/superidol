/* 
    檔案：http.js
    用途：HTTP 客戶端配置
    功能：
    - 配置 axios 實例
    - 設置請求攔截器
    - 設置響應攔截器
*/
import axios from 'axios';

const http = axios.create({
    baseURL: '/api',  // 使用代理，避免跨域問題
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json'
    }
});

// 請求攔截器
http.interceptors.request.use(
    config => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    error => Promise.reject(error)
);

// 響應攔截器
http.interceptors.response.use(
    response => response,
    error => {
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    localStorage.removeItem('token');
                    window.location.href = '/';
                    break;
                case 403:
                    console.error('沒有權限訪問');
                    break;
                case 404:
                    console.error('請求的資源不存在');
                    break;
                case 500:
                    console.error('伺服器錯誤');
                    break;
                default:
                    console.error('發生錯誤:', error.message);
            }
        }
        return Promise.reject(error);
    }
);

export default http; 