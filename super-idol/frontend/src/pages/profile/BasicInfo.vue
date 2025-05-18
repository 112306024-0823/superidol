<template>
  <div class="basic-info-page">
    <div class="container">
      <h1 class="page-title">個人資料</h1>
      
      <div class="profile-form-container">
        <form @submit.prevent="saveProfile" class="profile-form">
          <div class="form-section">
            <h2 class="section-title">基本資料</h2>
            
            <div class="form-row">
              <div class="form-group">
                <label for="name" class="form-label">姓名</label>
                <input 
                  id="name"
                  v-model="profile.name"
                  type="text"
                  class="form-input"
                  placeholder="您的姓名"
                />
              </div>
              
              <div class="form-group">
                <label for="gender" class="form-label">性別</label>
                <select 
                  id="gender"
                  v-model="profile.gender"
                  class="form-select"
                >
                  <option value="">請選擇</option>
                  <option value="male">男性</option>
                  <option value="female">女性</option>
                  <option value="other">其他</option>
                </select>
              </div>
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="birthdate" class="form-label">出生日期</label>
                <input 
                  id="birthdate"
                  v-model="profile.birthdate"
                  type="date"
                  class="form-input"
                />
              </div>
              
              <div class="form-group">
                <label for="email" class="form-label">電子郵件</label>
                <input 
                  id="email"
                  v-model="profile.email"
                  type="email"
                  class="form-input"
                  placeholder="您的電子郵件"
                  disabled
                />
              </div>
            </div>
          </div>
          
          <div class="form-section">
            <h2 class="section-title">身體數據</h2>
            
            <div class="form-row">
              <div class="form-group">
                <label for="height" class="form-label">身高 (cm)</label>
                <input 
                  id="height"
                  v-model.number="profile.height"
                  type="number"
                  class="form-input"
                  placeholder="身高"
                  min="100"
                  max="250"
                />
              </div>
              
              <div class="form-group">
                <label for="weight" class="form-label">體重 (kg)</label>
                <input 
                  id="weight"
                  v-model.number="profile.weight"
                  type="number"
                  class="form-input"
                  placeholder="體重"
                  min="30"
                  max="300"
                  step="0.1"
                />
              </div>
            </div>
            
            <div class="form-group">
              <label for="activityLevel" class="form-label">活動水平</label>
              <select 
                id="activityLevel"
                v-model="profile.activityLevel"
                class="form-select"
              >
                <option value="sedentary">久坐不動 (辦公室工作)</option>
                <option value="light">輕度活動 (每週運動1-2次)</option>
                <option value="moderate">中度活動 (每週運動3-5次)</option>
                <option value="active">高度活動 (每週運動6-7次)</option>
                <option value="veryActive">極高活動 (每天多次高強度運動)</option>
              </select>
            </div>
          </div>
          
          <div class="form-section">
            <h2 class="section-title">營養目標</h2>
            
            <div class="form-group">
              <label for="calorieGoal" class="form-label">每日卡路里目標</label>
              <input 
                id="calorieGoal"
                v-model.number="profile.calorieGoal"
                type="number"
                class="form-input"
                placeholder="卡路里目標"
                min="1000"
                max="5000"
              />
            </div>
            
            <div class="form-row">
              <div class="form-group">
                <label for="proteinGoal" class="form-label">蛋白質目標 (g)</label>
                <input 
                  id="proteinGoal"
                  v-model.number="profile.proteinGoal"
                  type="number"
                  class="form-input"
                  placeholder="蛋白質目標"
                  min="0"
                />
              </div>
              
              <div class="form-group">
                <label for="carbsGoal" class="form-label">碳水化合物目標 (g)</label>
                <input 
                  id="carbsGoal"
                  v-model.number="profile.carbsGoal"
                  type="number"
                  class="form-input"
                  placeholder="碳水化合物目標"
                  min="0"
                />
              </div>
              
              <div class="form-group">
                <label for="fatGoal" class="form-label">脂肪目標 (g)</label>
                <input 
                  id="fatGoal"
                  v-model.number="profile.fatGoal"
                  type="number"
                  class="form-input"
                  placeholder="脂肪目標"
                  min="0"
                />
              </div>
            </div>
          </div>
          
          <div class="form-actions">
            <button type="submit" class="btn btn-primary">儲存變更</button>
            <button type="button" class="btn btn-secondary" @click="resetForm">取消</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../../store/auth'

export default {
  name: 'BasicInfo',
  setup() {
    const authStore = useAuthStore()
    
    // 個人資料狀態
    const profile = ref({
      name: '',
      gender: '',
      birthdate: '',
      email: '',
      height: null,
      weight: null,
      activityLevel: 'moderate',
      calorieGoal: 2000,
      proteinGoal: 150,
      carbsGoal: 200,
      fatGoal: 65
    })
    
    // 載入個人資料
    onMounted(async () => {
      // 此處應該從API或store取得資料
      // 目前使用模擬資料
      if (authStore.user) {
        profile.value.name = authStore.user.name || ''
        profile.value.email = authStore.user.email || ''
      }
    })
    
    // 儲存個人資料
    const saveProfile = async () => {
      // 實際實作中應該呼叫API更新資料
      console.log('儲存資料:', profile.value)
      // TODO: 呼叫API儲存資料
      alert('資料已儲存！')
    }
    
    // 重置表單
    const resetForm = () => {
      // 重新載入原始資料
      onMounted()
    }
    
    return {
      profile,
      saveProfile,
      resetForm
    }
  }
}
</script>

<style scoped>

.basic-info-page {
  padding: 20px 0;
}

.page-title {
  margin-bottom: 24px;
  font-size: 28px;
  color: var(--text-color);
}

.profile-form-container {
  background-color: var(--card-bg);
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 24px;
}

.form-section {
  margin-bottom: 32px;
}

.section-title {
  font-size: 20px;
  margin-bottom: 16px;
  color: var(--primary-color);
  border-bottom: 1px solid #eee;
  padding-bottom: 8px;
}

.form-row {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 16px;
}

.form-group {
  flex: 1;
  min-width: 200px;
  margin-bottom: 16px;
}

.form-label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.form-input,
.form-select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.form-input:focus,
.form-select:focus {
  border-color: var(--primary-color);
  outline: none;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 32px;
}

/* 按鈕基本樣式 */
.btn {
  padding: 10px 20px;
  font-size: 16px;
  font-weight: 600;
  border-radius: 4px;
  cursor: pointer;
  border: 2px solid transparent;
  transition: all 0.3s ease;
  user-select: none;
}

.btn-primary {
  background-color: #f08c00; /* 橘色 */
  color: white;
  border-color: #f08c00;
}

.btn-primary:hover {
  background-color: white;
  color: #f08c00;
  border-color: #f08c00;
}

.btn-primary:hover {
  background-color: #d97706;
  color: white;
  border-color: #d97706;
}

.btn-secondary:hover {
  background-color: white;
  color: #d97706;
  border-color: #d97706;
}



@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
  }
  
  .form-group {
    width: 100%;
  }
}
</style> 