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
          
          <div class="form-section">
            <h2 class="section-title">食物偏好設置</h2>
            
            <div class="form-group">
              <label class="form-label">偏好食物類型</label>
              <div class="checkbox-group">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="profile.foodPreferences.chinese" />
                  <span>中式料理</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="profile.foodPreferences.western" />
                  <span>西式料理</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="profile.foodPreferences.japanese" />
                  <span>日式料理</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="profile.foodPreferences.korean" />
                  <span>韓式料理</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="profile.foodPreferences.vegetarian" />
                  <span>素食料理</span>
                </label>
              </div>
            </div>
            
            <div class="form-group">
              <label class="form-label">飲食限制</label>
              <div class="checkbox-group">
                <label class="checkbox-label">
                  <input type="checkbox" v-model="profile.dietaryRestrictions.glutenFree" />
                  <span>無麩質</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="profile.dietaryRestrictions.lactoseFree" />
                  <span>無乳糖</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="profile.dietaryRestrictions.nutFree" />
                  <span>無堅果</span>
                </label>
                <label class="checkbox-label">
                  <input type="checkbox" v-model="profile.dietaryRestrictions.seafoodAllergy" />
                  <span>海鮮過敏</span>
                </label>
              </div>
            </div>
            
            <div class="form-group">
              <label for="spicyLevel" class="form-label">辣度喜好</label>
              <div class="spicy-level-selector">
                <div class="spicy-level-options">
                  <label class="spicy-option" :class="{ active: profile.spicyLevel === 0 }">
                    <input type="radio" v-model="profile.spicyLevel" :value="0" />
                    <span>不吃辣</span>
                  </label>
                  <label class="spicy-option" :class="{ active: profile.spicyLevel === 1 }">
                    <input type="radio" v-model="profile.spicyLevel" :value="1" />
                    <span>微辣</span>
                  </label>
                  <label class="spicy-option" :class="{ active: profile.spicyLevel === 2 }">
                    <input type="radio" v-model="profile.spicyLevel" :value="2" />
                    <span>中辣</span>
                  </label>
                  <label class="spicy-option" :class="{ active: profile.spicyLevel === 3 }">
                    <input type="radio" v-model="profile.spicyLevel" :value="3" />
                    <span>重辣</span>
                  </label>
                </div>
                <div class="spicy-indicator">
                  <i class="fas fa-pepper-hot" v-for="n in profile.spicyLevel + 1" :key="n"></i>
                </div>
              </div>
            </div>
            
            <div class="form-group">
              <label for="priceRange" class="form-label">價格預算</label>
              <div class="price-range">
                <span>低價</span>
                <input 
                  type="range" 
                  v-model.number="profile.priceRange" 
                  min="1" 
                  max="5" 
                  class="range-slider" 
                />
                <span>高價</span>
              </div>
              <div class="price-indicator">
                <i class="fas fa-dollar-sign" v-for="n in profile.priceRange" :key="n"></i>
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
      fatGoal: 65,
      foodPreferences: {
        chinese: true,
        western: true,
        japanese: false,
        korean: false,
        vegetarian: false
      },
      dietaryRestrictions: {
        glutenFree: false,
        lactoseFree: false,
        nutFree: false,
        seafoodAllergy: false
      },
      spicyLevel: 1,
      priceRange: 3
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
      
      // 存储用户资料到 localStorage，以便在用户偏好和食物推荐中使用
      localStorage.setItem('userProfile', JSON.stringify(profile.value))
      
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

/* 新增樣式 */
.checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 4px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
  padding: 6px 12px;
  border-radius: 16px;
  background-color: #f5f5f5;
  transition: all 0.2s;
}

.checkbox-label:hover {
  background-color: #efefef;
}

.checkbox-label input[type="checkbox"] {
  margin-right: 8px;
}

.checkbox-label input[type="checkbox"]:checked + span {
  color: var(--primary-color);
  font-weight: 500;
}

.spicy-level-selector {
  margin-top: 8px;
}

.spicy-level-options {
  display: flex;
  gap: 10px;
}

.spicy-option {
  flex: 1;
  cursor: pointer;
  padding: 8px;
  border-radius: 4px;
  background-color: #f5f5f5;
  text-align: center;
  transition: all 0.2s;
}

.spicy-option input[type="radio"] {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.spicy-option.active {
  background-color: var(--primary-color);
  color: white;
}

.spicy-indicator {
  margin-top: 8px;
  color: #ff4d4f;
}

.price-range {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 8px;
}

.range-slider {
  flex: 1;
}

.price-indicator {
  margin-top: 8px;
  color: #389e0d;
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