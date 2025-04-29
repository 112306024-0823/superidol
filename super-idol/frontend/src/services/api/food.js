/* 
    檔案：food.js
    用途：食物相關的 API
    功能：
    - 食物列表的 CRUD 操作
    - 食物分類管理
    - 食物營養資訊管理
*/
import http from '../http';

export const foodAPI = {
    // 獲取所有食物
    getAll: () => http.get('/foods'),
    
    // 獲取單個食物
    getById: (id) => http.get(`/foods/${id}`),
    
    // 新增食物
    create: (data) => http.post('/foods', data),
    
    // 更新食物
    update: (id, data) => http.put(`/foods/${id}`, data),
    
    // 刪除食物
    delete: (id) => http.delete(`/foods/${id}`),
    
    // 獲取食物分類
    getCategories: () => http.get('/foods/categories'),
    
    // 獲取食物營養資訊
    getNutrition: (id) => http.get(`/foods/${id}/nutrition`)
}; 