import axios from 'axios'

// 創建 axios 實例
const api = axios.create({
  baseURL: '/api', // 代理設置必須對應此基礎URL
  timeout: 10000, // 請求超時時間 10 秒
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// 打印詳細的請求信息以便調試
api.interceptors.request.use(
  (config) => {
    console.log(`API請求: ${config.method.toUpperCase()} ${config.baseURL}${config.url}`, config.data || {});
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    console.error('請求錯誤:', error);
    return Promise.reject(error)
  }
)

// 響應攔截器 - 處理常見錯誤
api.interceptors.response.use(
  (response) => {
    console.log(`API回應 [${response.status}]:`, response.data);
    return response
  },
  (error) => {
    console.error('回應錯誤詳情:', error.response?.data || error.message);
    const { response } = error
    
    // 未驗證 (401) - 清除 token 並重新導向到登入頁面
    if (response && response.status === 401) {
      localStorage.removeItem('token')
      // 避免在登入頁面時重新導向
      if (window.location.pathname !== '/login') {
        window.location.href = '/login'
      }
    }
    
    // 伺服器錯誤 (500) - 通用錯誤處理
    if (response && response.status >= 500) {
      console.error('服務器錯誤:', error)
      // 可以在這裡顯示通用錯誤提示
    }
    
    return Promise.reject(error)
  }
)

export default api 