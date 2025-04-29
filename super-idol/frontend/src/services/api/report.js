/* 
    檔案：report.js
    用途：報告相關的 API
    功能：
    - 週報表管理
    - 日報表管理
    - 營養分析報告
*/
import http from '../http';

export const reportAPI = {
    // 獲取週報表
    getWeekly: (week) => http.get(`/reports/weekly/${week}`),
    
    // 獲取日報表
    getDaily: (date) => http.get(`/reports/daily/${date}`),
    
    // 獲取營養分析
    getAnalysis: (startDate, endDate) => 
        http.get(`/reports/analysis?start=${startDate}&end=${endDate}`),
    
    // 匯出報告
    exportReport: (type, data) => 
        http.post(`/reports/export/${type}`, data, {
            responseType: 'blob'
        })
}; 