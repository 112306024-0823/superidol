/* 
    檔案：api.js
    用途：API 服務
    功能：
    - 封裝所有 API 請求
    - 處理請求錯誤
    - 管理認證狀態
*/
import axios from 'axios';

const api = axios.create({
    baseURL: process.env.VUE_APP_API_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

// 請求攔截器
api.interceptors.request.use(
    config => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    error => {
        return Promise.reject(error);
    }
);

// 響應攔截器
api.interceptors.response.use(
    response => response,
    error => {
        if (error.response?.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export const userAPI = {
    // 用戶認證
    login: async (credentials) => {
        const response = await api.post('/auth/login', credentials);
        return response.data;
    },
    
    register: async (userData) => {
        const response = await api.post('/auth/register', userData);
        return response.data;
    },
    
    // 用戶資料
    getProfile: async () => {
        const response = await api.get('/user/profile');
        return response.data;
    },
    
    updateProfile: async (profileData) => {
        const response = await api.put('/user/profile', profileData);
        return response.data;
    },
    
    changePassword: async (passwordData) => {
        const response = await api.put('/user/password', passwordData);
        return response.data;
    }
};

export const foodAPI = {
    // 食物相關 API
    search: async (query) => {
        const response = await api.get('/food/search', { params: query });
        return response.data;
    },
    
    getDetails: async (id) => {
        const response = await api.get(`/food/${id}`);
        return response.data;
    }
};

export const reportAPI = {
    // 報告相關 API
    getDailyReport: async (date) => {
        const response = await api.get('/report/daily', { params: { date } });
        return response.data;
    },
    
    getWeeklyReport: async (startDate) => {
        const response = await api.get('/report/weekly', { params: { startDate } });
        return response.data;
    },
    
    getMonthlyReport: async (month) => {
        const response = await api.get('/report/monthly', { params: { month } });
        return response.data;
    }
};

export default api; 