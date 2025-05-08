<template>
  <div class="register-page">
    <el-card class="auth-container">
      <div class="auth-header">
        <h1>Super Idol</h1>
        <p>創建新帳戶</p>
      </div>
      
      <el-alert v-if="authError" type="error" :title="authError" show-icon />
      
      <el-form 
        @submit.native.prevent="handleRegister" 
        class="auth-form" 
        :model="form" 
        status-icon
      >
        <el-form-item label="姓名" prop="name">
          <el-input 
            v-model="form.name"
            placeholder="請輸入您的姓名"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item label="電子郵件" prop="email">
          <el-input 
            v-model="form.email"
            type="email" 
            placeholder="請輸入電子郵件"
            prefix-icon="Message"
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
        
        <el-form-item label="確認密碼" prop="confirmPassword">
          <el-input 
            v-model="form.confirmPassword"
            type="password" 
            placeholder="請再次輸入密碼"
            prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            :loading="isLoading" 
            @click="handleRegister" 
            class="register-btn"
          >
            {{ isLoading ? '註冊中...' : '註冊' }}
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="auth-footer">
        <p>
          已有帳戶？
          <router-link to="/login">
            <el-link type="primary">立即登入</el-link>
          </router-link>
        </p>
      </div>
    </el-card>
  </div>
</template>

<script>
import { reactive, computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth'
import { User, Message, Lock } from '@element-plus/icons-vue'

export default {
  name: 'RegisterPage',
  components: { User, Message, Lock },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const form = reactive({
      name: '',
      email: '',
      password: '',
      confirmPassword: ''
    })
    
    const localError = ref('')
    
    const handleRegister = async () => {
      if (form.password !== form.confirmPassword) {
        localError.value = '兩次輸入的密碼不一致'
        return
      }
      
      localError.value = ''
      
      try {
        await authStore.register({
          name: form.name,
          email: form.email,
          password: form.password
        })
        
        // 註冊成功，導航到儀表板
        router.push('/dashboard')
      } catch (error) {
        console.error('註冊失敗:', error)
      }
    }
    
    const authError = computed(() => {
      return localError.value || authStore.error
    })
    
    return {
      form,
      handleRegister,
      isLoading: computed(() => authStore.isLoading),
      authError
    }
  }
}
</script>

<style scoped>
.register-page {
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
  color: #ffa940;
  margin-bottom: 8px;
}

.auth-form {
  margin-top: 20px;
}

.register-btn {
  width: 100%;
}

.auth-footer {
  text-align: center;
  margin-top: 16px;
}
</style>