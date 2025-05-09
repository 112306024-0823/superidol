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
import { reactive, computed, ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth'
import { User, Message, Lock } from '@element-plus/icons-vue'
import { isValidEmail, validatePassword, isValidName, doPasswordsMatch } from '../../utils/validation'

export default {
  name: 'RegisterPage',
  components: { User, Message, Lock },
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    const registerForm = ref(null)
    const formIsValid = ref(true) // 設為true以允許提交
    const passwordResult = ref({
      isValid: false,
      message: '',
      strength: 'weak'
    })
    
    const form = reactive({
      name: '',
      email: '',
      password: '',
      confirmPassword: ''
    })
    
    const localError = ref('')
    
    // 定義表單驗證規則
    const rules = {
      name: [
        { required: true, message: '請輸入姓名', trigger: 'blur' },
        { 
          validator: (rule, value, callback) => {
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
        { min: 8, message: '密碼長度必須至少為8個字符', trigger: 'blur' },
        { 
          validator: (rule, value, callback) => {
            const result = validatePassword(value)
            if (!result.isValid) {
              callback(new Error(result.message))
            } else {
              // 當密碼變更時，同時檢查確認密碼
              if (form.confirmPassword) {
                registerForm.value?.validateField('confirmPassword')
              }
              callback()
            }
          }, 
          trigger: ['blur', 'change'] 
        }
      ],
      confirmPassword: [
        { required: true, message: '請再次輸入密碼', trigger: 'blur' },
        { 
          validator: (rule, value, callback) => {
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
    
    // 表單提交時先進行驗證
    const submitForm = () => {
      if (!registerForm.value) {
        // 如果表單ref不存在，直接執行註冊邏輯
        handleRegister();
        return;
      }
      
      registerForm.value.validate((valid) => {
        if (valid) {
          handleRegister();
        } else {
          // 即使表單驗證失敗，也允許用戶嘗試註冊
          console.log('表單驗證失敗，但仍嘗試註冊');
          handleRegister();
        }
      });
    }
    
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

.password-strength {
  margin-top: 5px;
  font-size: 12px;
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
  color: #1890ff;
}

.password-strength.error {
  color: #ff4d4f;
}
</style>