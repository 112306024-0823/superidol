<template>
  <div class="preferences-page">
    <el-card class="auth-container">
      <div class="auth-header">
        <h1>Super Idol</h1>
        <p>設定您的偏好</p>
      </div>
      
      <el-alert v-if="authError" type="error" :title="authError" show-icon />
      
      <div class="progress-bar">
        <div class="step completed">基本資訊</div>
        <div class="step active">偏好設定</div>
        <div class="step">完成</div>
      </div>
      
      <!-- 顯示載入中狀態 -->
      <div v-if="!dataLoaded" class="loading-container">
        <el-icon class="is-loading"><Loading /></el-icon>
        <p>載入中，請稍候...</p>
      </div>
      
      <!-- 已載入才顯示表單 -->
      <div v-if="dataLoaded">
        <el-form 
          class="preferences-form" 
          :model="preferences"
          ref="preferencesForm"
        >
          <!-- 預算和熱量限制 -->
          <div class="section">
            <h3 class="section-title">個人設定</h3>
            
            <el-form-item label="每餐預算 *" prop="budget">
              <el-input-number 
                v-model="budget" 
                :min="0" 
                placeholder="請輸入預算（必填）" 
                controls-position="right"
                style="width: 100%;"
              />
            </el-form-item>

            <el-form-item label="每週熱量限制 *" prop="calorieLimit">
              <el-input-number 
                v-model="calorieLimit" 
                :min="0" 
                placeholder="請輸入每週熱量限制（必填）" 
                controls-position="right"
                style="width: 100%;"
              />
            </el-form-item>
          </div>
          
          <!-- 食物偏好 -->
          <div class="section">
            <h3 class="section-title">飲食偏好</h3>
            
            <!-- 店家偏好 -->
            <el-form-item label="店家偏好">
              <div class="checkbox-group">
                <el-checkbox v-model="preferences.storePreferences.fastFood">速食店</el-checkbox>
                <el-checkbox v-model="preferences.storePreferences.beverageShop">手搖飲</el-checkbox>
              </div>
            </el-form-item>
            
            <!-- 食物類型偏好 -->
            <el-form-item label="食物類型偏好">
              <div class="checkbox-group">
                <div class="checkbox-row">
                  <h4>速食店:</h4>
                  <el-checkbox v-model="preferences.foodTypePreferences.burger">漢堡</el-checkbox>
                  <el-checkbox v-model="preferences.foodTypePreferences.friedChicken">炸雞</el-checkbox>
                  <el-checkbox v-model="preferences.foodTypePreferences.fries">薯條</el-checkbox>
                  <el-checkbox v-model="preferences.foodTypePreferences.sandwich">三明治</el-checkbox>
                </div>
                <div class="checkbox-row">
                  <h4>手搖飲:</h4>
                  <el-checkbox v-model="preferences.foodTypePreferences.milkTea">奶茶</el-checkbox>
                  <el-checkbox v-model="preferences.foodTypePreferences.fruitTea">果茶</el-checkbox>
                  <el-checkbox v-model="preferences.foodTypePreferences.coffee">咖啡</el-checkbox>
                </div>
              </div>
            </el-form-item>
          </div>
          
          <!-- 運動偏好 -->
          <div class="section">
            <h3 class="section-title">運動偏好</h3>
            <el-form-item label="喜好的運動類型">
              <div class="checkbox-group">
                <el-checkbox v-model="preferences.exercisePreferences.running">跑步</el-checkbox>
                <el-checkbox v-model="preferences.exercisePreferences.swimming">游泳</el-checkbox>
                <el-checkbox v-model="preferences.exercisePreferences.cycling">騎自行車</el-checkbox>
                <el-checkbox v-model="preferences.exercisePreferences.walking">健走</el-checkbox>
                <el-checkbox v-model="preferences.exercisePreferences.basketball">籃球</el-checkbox>
                <el-checkbox v-model="preferences.exercisePreferences.weightlifting">重訓</el-checkbox>
                <el-checkbox v-model="preferences.exercisePreferences.yoga">瑜伽</el-checkbox>
              </div>
            </el-form-item>
          </div>
          
          <!-- 餐廳偏好 -->
          <div class="section">
            <h3 class="section-title">餐廳偏好</h3>
            <el-form-item label="喜好的餐廳類型">
              <div class="checkbox-group restaurant-types">
                <el-checkbox v-for="restaurant in popularRestaurants" 
                  :key="restaurant.id" 
                  v-model="preferences.restaurantPreferences[restaurant.id]">
                  {{ restaurant.name }}
                </el-checkbox>
              </div>
            </el-form-item>
          </div>
          
          <div class="note">
            <p>* 所有偏好設定均為選填，我們會根據您的偏好為您推薦內容</p>
          </div>
          
          <div class="form-actions">
            <el-button @click="goBack">返回</el-button>
            <el-button 
              type="primary" 
              :loading="isLoading" 
              @click="submitForm"
            >
              {{ isLoading ? '提交中...' : '完成註冊' }}
            </el-button>
          </div>
        </el-form>
      </div>
    </el-card>
  </div>
</template>

<script>
import { reactive, ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../../store/auth'
import { ElMessage } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'

export default {
  name: 'UserPreferences',
  components: { Loading },
  setup() {
    const router = useRouter()
    const route = useRoute()
    const authStore = useAuthStore()
    const preferencesForm = ref(null)
    const localError = ref('')
    
    // 表單數據
    const budget = ref(200) // 預設值
    const calorieLimit = ref(12000) // 預設值
    const dataLoaded = ref(false)
    const registrationData = ref({})
    
    // 熱門餐廳列表
    const popularRestaurants = [
      { id: 'mcdonalds', name: '麥當勞' },
      { id: 'kfc', name: '肯德基' },
      { id: 'burgerking', name: '漢堡王' },
      { id: 'mosburger', name: '摩斯漢堡' },
      { id: 'coco', name: 'COCO都可' },
      { id: 'milkshop', name: '迷客夏' },
      { id: 'starbucks', name: '星巴克' },
      { id: '50lan', name: '50嵐' }
    ]
    
    // 偏好設置
    const preferences = reactive({
      storePreferences: {
        fastFood: true,
        beverageShop: true
      },
      foodTypePreferences: {
        burger: false,
        friedChicken: false,
        fries: false,
        sandwich: false,
        milkTea: false,
        fruitTea: false,
        coffee: false
      },
      exercisePreferences: {
        running: false,
        swimming: false,
        cycling: false,
        walking: false,
        basketball: false,
        weightlifting: false,
        yoga: false
      },
      restaurantPreferences: {
        mcdonalds: false,
        kfc: false,
        burgerking: false,
        mosburger: false,
        coco: false,
        milkshop: false,
        starbucks: false,
        '50lan': false
      }
    })
    
    // 初始化數據
    onMounted(() => {
      try {
        // 檢查是否有註冊數據
        const storedData = sessionStorage.getItem('registrationData')
        if (!storedData) {
          ElMessage.warning('請先完成基本資訊設定')
          router.push('/register')
          return
        }
        
        // 解析並儲存數據
        registrationData.value = JSON.parse(storedData)
        console.log('成功載入註冊數據:', registrationData.value)
        
        // 標記數據已載入
        dataLoaded.value = true
      } catch (error) {
        console.error('載入註冊數據失敗:', error)
        ElMessage.error('載入數據失敗，請重新填寫基本資訊')
        router.push('/register')
      }
    })
    
    // 提交表單
    const submitForm = async () => {
      try {
        // 驗證必填欄位
        if (budget.value === null || budget.value === '' || budget.value === 0) {
          ElMessage.warning('請填寫每餐預算')
          return
        }
        
        if (calorieLimit.value === null || calorieLimit.value === '' || calorieLimit.value === 0) {
          ElMessage.warning('請填寫每週熱量限制')
          return
        }
        
        // 收集食物偏好
        const foodPreferencesList = []
        for (const [key, value] of Object.entries(preferences.foodTypePreferences)) {
          if (value) foodPreferencesList.push(key)
        }
        
        // 收集運動偏好
        const exercisePreferencesList = []
        for (const [key, value] of Object.entries(preferences.exercisePreferences)) {
          if (value) exercisePreferencesList.push(key)
        }
        
        // 收集餐廳偏好
        const restaurantPreferencesList = []
        for (const [key, value] of Object.entries(preferences.restaurantPreferences)) {
          if (value) restaurantPreferencesList.push(key)
        }
        
        // 準備最終註冊數據
        const completeData = {
          ...registrationData.value,
          budget: budget.value,
          calorieLimit: calorieLimit.value,
          foodPreference: foodPreferencesList.join(','),
          exercisePreference: exercisePreferencesList.join(','),
          restaurantPreference: restaurantPreferencesList.join(',')
        }
        
        console.log('準備提交註冊數據:', completeData)
        
        // 提交註冊
        await authStore.register(completeData)
        
        // 清除臨時數據
        sessionStorage.removeItem('registrationData')
        
        // 顯示成功訊息
        ElMessage.success('註冊成功！')
        
        // 等待一小段時間，確保狀態更新
        setTimeout(() => {
          // 檢查 token 是否已存儲
          if (localStorage.getItem('token')) {
            console.log('檢測到 token，導航到儀表板')
            // 導航到儀表板
            router.push('/dashboard')
          } else {
            console.warn('未檢測到 token，導航到登入頁面')
            // 導航到登入頁面
            router.push('/login')
          }
        }, 1000)  // 等待 1 秒
      } catch (error) {
        console.error('註冊失敗:', error)
        // 處理特定錯誤類型
        if (error.response && error.response.status === 409) {
          // 清除sessionStorage避免資料殘留
          sessionStorage.removeItem('registrationData')
          
          localError.value = '這個電子郵件已經註冊過，請使用其他電子郵件或直接登入'
          ElMessage({
            message: '這個電子郵件已經註冊過，是否要直接登入?',
            type: 'warning',
            showClose: true,
            duration: 0, // 不自動關閉
            center: true,
            customClass: 'email-exists-warning',
            dangerouslyUseHTMLString: true,
            message: `
              <div style="text-align: center; padding: 10px;">
                <h3 style="margin-bottom: 10px;">這個電子郵件已經註冊過</h3>
                <p style="margin-bottom: 15px;">您可以嘗試使用此帳號直接登入，或返回使用其他電子郵件。</p>
                <div style="display: flex; justify-content: center; gap: 10px;">
                  <button id="go-to-login-btn" style="
                    background-color: #f08c00; 
                    color: white; 
                    border: none; 
                    padding: 8px 15px; 
                    border-radius: 4px;
                    cursor: pointer;
                  ">前往登入</button>
                  <button id="try-other-email-btn" style="
                    background-color: #909399; 
                    color: white; 
                    border: none; 
                    padding: 8px 15px; 
                    border-radius: 4px;
                    cursor: pointer;
                  ">更換電子郵件</button>
                </div>
              </div>
            `
          })
          
          // 添加按鈕點擊事件監聽器
          setTimeout(() => {
            const loginBtn = document.getElementById('go-to-login-btn')
            const tryOtherBtn = document.getElementById('try-other-email-btn')
            
            if (loginBtn) {
              loginBtn.addEventListener('click', () => {
                ElMessage.closeAll()
                router.push('/login')
              })
            }
            
            if (tryOtherBtn) {
              tryOtherBtn.addEventListener('click', () => {
                ElMessage.closeAll()
                router.push('/register')
              })
            }
          }, 100)
          
        } else if (error.message && error.message.includes('timeout')) {
          localError.value = '伺服器回應超時，請稍後再試'
          ElMessage.error('伺服器回應超時，請稍後再試')
        } else {
          localError.value = '註冊失敗，請稍後再試'
          ElMessage.error('註冊失敗，請稍後再試')
        }
      }
    }
    
    // 返回上一頁
    const goBack = () => {
      router.push('/register')
    }
    
    // 返回模板需要的所有數據和方法
    return {
      budget,
      calorieLimit,
      preferences,
      popularRestaurants,
      dataLoaded,
      submitForm,
      goBack,
      preferencesForm,
      isLoading: computed(() => authStore.isLoading),
      authError: computed(() => localError.value || authStore.error)
    }
  }
}
</script>

<style scoped>
.preferences-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 40px 0;
  background-color: #f5f7fa;
}

.auth-container {
  width: 100%;
  max-width: 700px;
}

.auth-header {
  text-align: center;
  margin-bottom: 24px;
}

.auth-header h1 {
  margin-bottom: 8px;
  color: #f08c00;
  font-weight: 700;
  font-size: 2.4rem;
}

.auth-header p {
  color: #f08c00;
  font-weight: 600;
  font-size: 1.2rem;
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

.section {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.section-title {
  color: #606266;
  font-size: 18px;
  margin-bottom: 16px;
  font-weight: 500;
}

.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.checkbox-row {
  width: 100%;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 12px;
}

.checkbox-row h4 {
  margin: 0;
  font-size: 14px;
  color: #606266;
  min-width: 70px;
}

.restaurant-types {
  max-height: 150px;
  overflow-y: auto;
}

.note {
  font-size: 14px;
  color: #909399;
  margin: 20px 0;
  font-style: italic;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 50px 0;
}

.loading-container .el-icon {
  font-size: 48px;
  color: #f08c00;
  margin-bottom: 20px;
}

.loading-container p {
  color: #606266;
  font-size: 16px;
}

@media (max-width: 600px) {
  .auth-container {
    padding: 15px;
  }
  
  .checkbox-group {
    gap: 8px;
  }
  
    .checkbox-row h4 {      min-width: 100%;      margin-bottom: 8px;    }  }</style>