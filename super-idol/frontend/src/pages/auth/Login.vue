<template>
  <div class="login-page">
    <el-card class="auth-container">
      <div class="auth-header">
        <h1>速per Idol</h1>
        <p>歡迎回來</p>
      </div>
      
      <el-alert v-if="authError" type="error" :title="authError" show-icon />
      
      <el-form @submit.native.prevent="handleLogin" class="auth-form" :model="form" status-icon>
        <el-form-item label="電子郵件" prop="email">
          <el-input 
            v-model="form.email" 
            placeholder="請輸入電子郵件"
            prefix-icon="Message"
            type="email"
          />
        </el-form-item>
        
        <el-form-item label="密碼" prop="password">
          <el-input 
            v-model="form.password"
            type="password" 
            placeholder="請輸入密碼"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            :loading="isLoading" 
            @click="handleLogin" 
            class="login-btn"
          >
            {{ isLoading ? '登入中...' : '登入' }}
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="auth-footer">
        <p>
          還沒有帳戶？
          <router-link to="/register">
            <el-link type="primary">立即註冊</el-link>
          </router-link>
        </p>
      </div>
    </el-card>
  </div>
</template>

<script>
import { ref, computed, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth'
import { Message, Lock } from '@element-plus/icons-vue'

export default {
  name: 'LoginPage',
  components: { Message, Lock },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const form = reactive({
      email: '',
      password: ''
    })
    
    const handleLogin = async () => {
      try {
        await authStore.login({
          email: form.email,
          password: form.password
        })
        
        // 登入成功，導航到儀表板
        router.push('/dashboard')
      } catch (error) {
        console.error('登入失敗:', error)
      }
    }
    
    const authError = computed(() => authStore.error)
    
    return {
      form,
      handleLogin,
      isLoading: computed(() => authStore.isLoading),
      authError
    }
  }
}
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f5f7fa;
}

.auth-container {
  width: 100%;
  max-width: 440px;
}

.auth-header {
  text-align: center;
  margin-bottom: 24px;
}

.auth-header h1 {
  margin-bottom: 8px;
  color: #409eff;
}

.auth-form {
  margin-top: 20px;
}

.login-btn {
  width: 100%;
}

.auth-footer {
  text-align: center;
  margin-top: 16px;
}
</style>