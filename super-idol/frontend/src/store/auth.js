import { defineStore } from 'pinia'
import api from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    isLoading: false,
    error: null
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
    hasError: (state) => !!state.error,
  },
  
  actions: {
    async login(credentials) {
      this.isLoading = true
      this.error = null
      
      try {
        // 呼叫後端 API 進行登入，確保路徑正確
        const response = await api.post('/auth/login', credentials)
        
        // 儲存 token 到 localStorage
        const token = response.data.access_token
        localStorage.setItem('token', token)
        
        // 更新 state
        this.token = token
        this.user = response.data.user
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || '登入失敗，請檢查您的憑證'
        throw error
      } finally {
        this.isLoading = false
      }
    },
    
    async register(userData) {
      this.isLoading = true
      this.error = null
      
      try {
        // 呼叫後端 API 進行註冊，確保路徑正確
        console.log('正在發送註冊請求:', userData);
        const response = await api.post('/auth/signup', userData)
        
        // 儲存 token 到 localStorage
        const token = response.data.access_token
        localStorage.setItem('token', token)
        
        // 更新 state
        this.token = token
        this.user = response.data.user
        
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || '註冊失敗，請稍後再試'
        throw error
      } finally {
        this.isLoading = false
      }
    },
    
    async logout() {
      try {
        // 可選：通知後端使 token 失效
        if (this.token) {
          await api.post('/auth/logout')
        }
      } catch (error) {
        console.error('登出 API 請求失敗:', error)
      } finally {
        // 無論 API 呼叫是否成功，都清除前端的 token 和使用者資訊
        localStorage.removeItem('token')
        this.token = null
        this.user = null
      }
    },
    
    async fetchUserData() {
      if (!this.token) return
      
      this.isLoading = true
      
      try {
        const response = await api.get('/auth/user')
        this.user = response.data
        return response.data
      } catch (error) {
        console.error('獲取使用者資料失敗:', error)
        // 如果獲取用戶資料失敗，可能是 token 已失效
        if (error.response?.status === 401) {
          this.logout()
        }
      } finally {
        this.isLoading = false
      }
    },
    
    async updateUserProfile(profileData) {
      if (!this.token) return
      
      this.isLoading = true
      this.error = null
      
      try {
        const response = await api.put('/auth/profile', profileData)
        this.user = { ...this.user, ...response.data }
        return response.data
      } catch (error) {
        this.error = error.response?.data?.message || '更新個人資料失敗'
        throw error
      } finally {
        this.isLoading = false
      }
    },
    
    clearError() {
      this.error = null
    }
  }
}) 