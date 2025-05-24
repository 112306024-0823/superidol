<template>
  <div class="register-page">
    <el-card class="auth-container">
      <div class="auth-header">
        <h1>Super Idol</h1>
        <p>創建新帳戶</p>
      </div>
      
      <el-alert v-if="authError" type="error" :title="authError" show-icon />
      
      <div class="progress-bar">
        <div class="step active">基本資訊</div>
        <div class="step">偏好設定</div>
        <div class="step">完成</div>
      </div>
      
      <el-form 
        @submit.native.prevent="handleRegister" 
        class="auth-form" 
        :model="form" 
        :rules="rules"
        ref="registerForm"
        status-icon
      >
        <el-form-item label="姓名" prop="name">
          <el-input 
            v-model="form.name"
            placeholder="請輸入您的姓名"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item label="體重 (kg) *" prop="weight">
          <el-input-number 
            v-model="form.weight" 
            :min="30" 
            :max="200"
            placeholder="請輸入您的體重（必填）" 
            controls-position="right"
            style="width: 100%;"
          />
        </el-form-item>

        <el-form-item label="電子郵件" prop="email">
          <el-input 
            v-model="form.email"
            type="email" 
            placeholder="請輸入電子郵件"
            prefix-icon="Message"
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
            @input="checkPasswordStrength"
          />
          <div v-if="passwordResult.isValid" class="password-strength" :class="passwordResult.strength">
            密碼強度: {{ passwordResult.message }}
          </div>
          <div v-else class="password-strength error">
            {{ passwordResult.message }}
          </div>
        </el-form-item>
        
        <el-form-item label="確認密碼" prop="confirmPassword">
          <el-input 
            v-model="form.confirmPassword"
            type="password" 
            placeholder="請再次輸入密碼"
            prefix-icon="Lock"
            show-password
            @input="validateConfirmPassword"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            :loading="isLoading" 
            @click="submitForm" 
            class="register-btn"
          >
            下一步
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
import { reactive, computed, ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth'
import { User, Message, Lock } from '@element-plus/icons-vue'
import { isValidEmail, validatePassword, isValidName, doPasswordsMatch } from '../../utils/validation'
import api from '../../services/api'
import { ElMessage } from 'element-plus'

export default {
  name: 'RegisterPage',
  components: { User, Message, Lock },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const registerForm = ref(null)
    const formIsValid = ref(true) // 設為true以允許提交
    const isSubmitAttempted = ref(false)
    const passwordResult = ref({
      isValid: false,
      message: '',
      strength: 'weak'
    })
    
    const form = reactive({
      name: '',           // 必填
      email: '',          // 必填
      password: '',       // 必填
      confirmPassword: '',
      weight: null,       // 必填（用於計算健康目標）
    })
    
    const localError = ref('')
    
    const rules = {
      name: [
        {
          validator: (rule, value, callback) => {
            if (!isSubmitAttempted.value && !value) {
              // 尚未提交且空白，不顯示錯誤
              callback()
              return
            }
            if (!value) {
              callback(new Error('請輸入姓名'))
            } else if (!isValidName(value)) {
              callback(new Error('姓名至少需要2個字符'))
            } else {
              callback()
            }
          },
          trigger: ['blur', 'change']
        }
      ],
      weight: [
        {
          validator: (rule, value, callback) => {
            if (!isSubmitAttempted.value && value == null) {
              callback()
              return
            }
            if (value == null || value === '') {
              callback(new Error('請輸入體重'))
            } else if (value < 20 || value > 200) {
              callback(new Error('體重需在合理範圍內'))
            } else {
              callback()
            }
          },
          trigger: ['blur', 'change']
        }
      ],
      email: [
        {
          validator: (rule, value, callback) => {
            if (!isSubmitAttempted.value && !value) {
              callback()
              return
            }
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
        {
          validator: (rule, value, callback) => {
            if (!isSubmitAttempted.value && !value) {
              callback()
              return
            }
            if (!value) {
              callback(new Error('請輸入密碼'))
            } else if (value.length < 8) {
              callback(new Error('密碼長度必須至少為8個字符'))
            } else {
              const result = validatePassword(value)
              if (!result.isValid) {
                callback(new Error(result.message))
              } else {
                callback()
              }
            }
          },
          trigger: ['blur', 'change']
        }
      ],
      confirmPassword: [
        {
          validator: (rule, value, callback) => {
            if (!isSubmitAttempted.value && !value) {
              callback()
              return
            }
            if (!value) {
              callback(new Error('請再次輸入密碼'))
            } else if (!doPasswordsMatch(form.password, value)) {
              callback(new Error('兩次輸入的密碼不一致'))
            } else {
              callback()
            }
          },
          trigger: ['blur', 'change']
        }
      ]
    }
    
    // 檢查密碼強度
    const checkPasswordStrength = () => {
      passwordResult.value = validatePassword(form.password)
      if (form.confirmPassword) {
        validateConfirmPassword()
      }
    }
    
    // 驗證確認密碼
    const validateConfirmPassword = () => {
      if (registerForm.value) {
        registerForm.value.validateField('confirmPassword')
      }
    }
    
    // 驗證電子郵件
    const validateEmail = () => {
      if (registerForm.value) {
        registerForm.value.validateField('email')
      }
    }
    
    const submitForm = () => {
      isSubmitAttempted.value = true
      if (!registerForm.value) {
        handleRegister()
        return
      }
      registerForm.value.validate(valid => {
        if (valid) {
          handleRegister()
        } else {
          console.log('表單驗證失敗，顯示錯誤訊息')
        }
      })
    }
    
    const handleRegister = async () => {
      if (form.password !== form.confirmPassword) {
        localError.value = '兩次輸入的密碼不一致'
        return
      }
      
      // 驗證所有必填欄位
      if (!form.name || !form.email || !form.password) {
        localError.value = '請填寫基本資料（姓名、電子郵件、密碼）'
        return
      }
      
      // 特別檢查體重
      if (form.weight === null || form.weight === '') {
        localError.value = '請填寫您的體重'
        if (registerForm.value) registerForm.value.validateField('weight')
        return
      }
      
      localError.value = ''
      
      // 創建包含必要註冊資訊的物件
      const registrationData = {
        name: form.name,
        email: form.email,
        password: form.password,
        weight: form.weight
      }
      
      // 將註冊資料保存到會話存儲
      sessionStorage.setItem('registrationData', JSON.stringify(registrationData))
      
      // 簡單導向偏好設置頁面，不通過路由參數傳遞數據
      router.push('/preferences')
    }
    
    const authError = computed(() => {
      return localError.value || authStore.error
    })
    
    // 監聽表單變化以更新表單有效性
    const validateForm = () => {
      if (registerForm.value) {
        registerForm.value.validate((valid) => {
          formIsValid.value = true; // 始終允許提交
        })
      }
    }
    
    // 監聽密碼變化
    watch(() => form.password, () => {
      checkPasswordStrength()
    })
    
    onMounted(() => {
      // 初始驗證表單
      validateForm()
    })
    
    return {
      form,
      rules,
      registerForm,
      handleRegister,
      submitForm,
      validateEmail,
      validateConfirmPassword,
      checkPasswordStrength,
      passwordResult,
      isSubmitAttempted,
      formIsValid,
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
  max-width: 700px;
  padding: 24px;
  box-shadow: 0 4px 12px rgb(0 0 0 / 0.1);
  border-radius: 8px;
}

.progress-bar {
  display: flex;
  justify-content: space-between;
  margin: 30px 0;
  position: relative;
}

.progress-bar::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #e0e0e0;
  z-index: 0;
}

.step {
  position: relative;
  width: 32%;
  text-align: center;
  padding: 10px;
  background-color: white;
  border: 2px solid #e0e0e0;
  border-radius: 20px;
  font-weight: 500;
  z-index: 1;
}

.step.completed {
  background-color: #f0fcf0;
  border-color: #67c23a;
  color: #67c23a;
}

.step.active {
  background-color: #fff8e6;
  border-color: #f08c00;
  color: #f08c00;
  font-weight: 600;
}

.auth-header {
  text-align: center;
  margin-bottom: 24px;
}

.auth-header h1 {
  color: #ffa940; /* 橘色 */
  margin-bottom: 8px;
  font-weight: 700;
  font-size: 2.2rem;
}

.auth-header p {
  color: #303133; /* 深灰/黑色 */
  font-weight: 600;
  font-size: 1.2rem;
}

.auth-form {
  margin-top: 20px;
}

/* 全部表單欄位垂直排列 */
.auth-form >>> .el-form-item {
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 16px;
}

/* 輸入框寬度全滿 */
.auth-form >>> .el-form-item__content {
  width: 100%;
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

/* 按鈕橘色風格 */
.register-btn {
  width: 100%;
  background-color: #ffa940;
  border-color: #ffa940;
  color: white;
  font-weight: 600;
  transition: background-color 0.3s ease;
  border-radius: 4px;
}

.register-btn:hover {
  background-color: #d48806;
  border-color: #d48806;
}

/* 立即登入橘色連結 */
.auth-footer .el-link {
  color: #ffa940 !important;
  font-weight: 600;
  cursor: pointer;
}

.auth-footer {
  text-align: center;
  margin-top: 16px;
  font-size: 14px;
}

/* 密碼強度提示 */
.password-strength {
  margin-top: 5px;
  font-size: 12px;
  font-weight: 600;
}

.password-strength.weak {
  color: #ff4d4f;
}

.password-strength.medium {
  color: #faad14;
}

.password-strength.good {
  color: #52c41a;
}

.password-strength.strong {
  color: #ffa940; /* 強調橘色 */
}

.password-strength.error {
  color: #ff4d4f;
}

/* 必填標記顏色 */
.auth-form >>> .el-form-item__label em {
  color: #ff4d4f;
}
</style>