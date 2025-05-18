<template>
  <div class="login-page">
    <el-card class="auth-container">
      <div class="auth-header">
        <h1>速per Idol</h1>
        <p>歡迎回來</p>
      </div>
      
      <el-alert v-if="authError" type="error" :title="authError" show-icon />
      
      <el-form @submit.native.prevent="handleLogin" class="auth-form" :model="form" :rules="rules" ref="loginForm" status-icon>
        <el-form-item label="電子郵件" prop="email">
          <el-input 
            v-model="form.email" 
            placeholder="請輸入電子郵件"
            prefix-icon="Message"
            type="email"
            @blur="validateEmail"
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
            @click="submitForm" 
            class="login-btn"
          >
            {{ isLoading ? '登入中...' : '登入' }}
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="connection-status">
        <span v-if="connectionStatus === 'waiting'" class="status waiting">正在測試API連接...</span>
        <span v-else-if="connectionStatus === 'success'" class="status success">API 連接正常</span>
        <span v-else-if="connectionStatus === 'error'" class="status error">API 連接失敗，請檢查後端是否運行</span>
      </div>
      
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
import { ref, computed, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth'
import { Message, Lock } from '@element-plus/icons-vue'
import { isValidEmail, validatePassword } from '../../utils/validation'
import api from '../../services/api'

export default {
  name: 'LoginPage',
  components: { Message, Lock },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const loginForm = ref(null)
    const formIsValid = ref(true) // 預設設為true以允許提交
    const connectionStatus = ref('waiting')
    
    const form = reactive({
      email: '',
      password: ''
    })

    // 定義表單驗證規則
    const rules = {
      email: [
        { required: true, message: '請輸入電子郵件', trigger: 'blur' },
        { 
          validator: (rule, value, callback) => {
            if (!value) {
              callback(new Error('請輸入電子郵件'))
            } else if (!isValidEmail(value)) {
              callback(new Error('請輸入有效的電子郵件地址'))
            } else {
              callback()
            }
          }, 
          trigger: ['blur', 'change'] 
        }
      ],
      password: [
        { required: true, message: '請輸入密碼', trigger: 'blur' },
        { min: 8, message: '密碼長度必須至少為8個字符', trigger: 'blur' }
      ]
    }
    
    // 表單提交時先進行驗證
    const submitForm = () => {
      if (!loginForm.value) {
        // 如果表單ref不存在，直接執行登入邏輯
        handleLogin();
        return;
      }
      
      loginForm.value.validate((valid) => {
        if (valid) {
          handleLogin();
        } else {
          // 即使表單驗證失敗，也允許嘗試登入
          console.log('表單驗證失敗，但仍嘗試登入');
          handleLogin();
        }
      });
    }
    
    // 即時驗證電子郵件
    const validateEmail = () => {
      if (loginForm.value) {
        loginForm.value.validateField('email');
      }
    }
    
    const handleLogin = async () => {
      try {
        console.log('嘗試登入...');
        await authStore.login({
          email: form.email,
          password: form.password
        })
        
        console.log('登入成功，導航到儀表板');
        // 登入成功，導航到儀表板
        router.push('/dashboard')
      } catch (error) {
        console.error('登入失敗:', error)
      }
    }
    
    // 測試API連接
    const testApiConnection = async () => {
      connectionStatus.value = 'waiting';
      try {
        await api.get('/api'); // 測試基本API連接
        connectionStatus.value = 'success';
      } catch (error) {
        console.error('API連接測試失敗:', error);
        connectionStatus.value = 'error';
      }
    }
    
    const authError = computed(() => authStore.error)
    
    // 監聽表單變化以更新表單有效性
    const validateForm = () => {
      if (loginForm.value) {
        loginForm.value.validate((valid) => {
          formIsValid.value = true; // 始終允許提交
        })
      }
    }
    
    onMounted(() => {
      // 初始驗證表單
      validateForm();
      // 測試API連接
      testApiConnection();
    })
    
    return {
      form,
      rules,
      loginForm,
      handleLogin,
      submitForm,
      validateEmail,
      formIsValid,
      connectionStatus,
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
  color: #f08c00; /* 橘色 */
  font-weight: 700;
  font-size: 2.4rem;
}

.auth-header p {
  color: #f08c00; /* 副標題橘色 */
  font-weight: 600;
  font-size: 1.2rem;
}

.login-btn {
  width: 100%;
  background-color: #f08c00; /* 橘色底 */
  border-color: #f08c00;
  color: white;
  font-weight: 600;
  transition: background-color 0.3s ease;
}

.login-btn:hover {
  background-color: #d97706; /* 深橘色 hover */
  border-color: #d97706;
}

.connection-status {
  text-align: center;
  margin-top: 10px;
  font-size: 13px;
  font-weight: 600;
}
.auth-footer .el-link {
  color: #f08c00 !important; /* 強制改成橘色 */
  font-weight: 600;
}

/* 讓表單標籤跟輸入框垂直排列 */
.auth-form >>> .el-form-item {
  flex-direction: column;
  align-items: flex-start;
}

.auth-form >>> .el-form-item__label {
  padding: 0 0 6px 0;
  font-weight: 600;
  color: #606266;
}

/* 輸入框寬度全滿 */
.auth-form >>> .el-form-item__content {
  width: 100%;
}

.status.waiting {
  color: #909399;
}

.status.success {
  color: #67c23a;
}

.status.error {
  color: #f56c6c;
}
</style>  