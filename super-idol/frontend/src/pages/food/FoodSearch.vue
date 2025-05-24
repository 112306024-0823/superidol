<template>
  <div class="food-search-page">
    <div class="container">
      <h1 class="page-title">食物搜尋</h1>

      <!-- 搜尋表單 -->
      <div class="search-form-container">
        <div class="search-form-card" @keydown.enter="handleSearch">
          <div class="search-form-grid">
            <!-- 第一行 -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">食物名稱</label>
                <div class="input-with-icon">
                  <i class="el-icon-food"></i>
                  <input type="text" class="form-control" placeholder="輸入食物名稱" v-model="filters.name" />
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">餐廳</label>
                <div class="input-with-icon">
                  <i class="el-icon-shop"></i>
                  <input type="text" class="form-control" placeholder="輸入餐廳名稱" v-model="filters.restaurant" />
                </div>
              </div>
            </div>
            
            <!-- 第二行 -->
            <div class="form-row">
              <div class="form-group">
                <label class="form-label">價格範圍</label>
                <div class="range-inputs">
                  <input type="number" class="form-control form-control-sm" placeholder="最低" v-model="filters.priceMin" />
                  <span class="range-separator">~</span>
                  <input type="number" class="form-control form-control-sm" placeholder="最高" v-model="filters.priceMax" />
                  <span class="unit">元</span>
                </div>
              </div>
              <div class="form-group">
                <label class="form-label">熱量範圍</label>
                <div class="range-inputs">
                  <input type="number" class="form-control form-control-sm" placeholder="最低" v-model="filters.calMin" />
                  <span class="range-separator">~</span>
                  <input type="number" class="form-control form-control-sm" placeholder="最高" v-model="filters.calMax" />
                  <span class="unit">大卡</span>
                </div>
              </div>
            </div>
            
            <!-- 第三行 -->
            <div class="form-row">
              <div class="form-group type-selector">
                <label class="form-label">餐點類型</label>
                <div class="type-buttons">
                  <button 
                    type="button" 
                    class="type-btn" 
                    :class="{ active: filters.type === '單點' }"
                    @click="toggleType('單點')"
                  >
                    單點
                  </button>
                  <button 
                    type="button" 
                    class="type-btn" 
                    :class="{ active: filters.type === '套餐' }"
                    @click="toggleType('套餐')"
                  >
                    套餐
                  </button>
                </div>
              </div>
              <div class="form-group search-btn-container">
                <button type="button" class="search-btn" @click="handleSearch">
                  <i class="el-icon-search"></i>
                  搜尋
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 搜尋結果 -->
      <div v-if="searchResults.length > 0" class="search-results">
        <h2 class="section-title">搜尋結果</h2>
        <div class="food-grid">
          <div class="food-card" v-for="(food, index) in searchResults" :key="index">
            <div class="food-card-content">
              <div class="food-info">
                <h3 class="food-name">{{ food.name }}</h3>
                <div class="food-details">
                  <div class="detail-item">
                    <i class="el-icon-shop"></i>
                    <span>{{ food.restaurant || '未知餐廳' }}</span>
                  </div>
                  <div class="detail-item">
                    <i class="el-icon-money"></i>
                    <span>{{ food.price }} 元</span>
                  </div>
                  <div class="detail-item">
                    <i class="el-icon-data-line"></i>
                    <span>{{ food.calories }} 大卡</span>
                  </div>
                  <div class="detail-item">
                    <i class="el-icon-food"></i>
                    <span>{{ food.food_type || '未分類' }}</span>
                  </div>
                  <div class="detail-item">
                    <i class="el-icon-menu"></i>
                    <span>{{ food.type }}</span>
                  </div>
                </div>
              </div>
              <div class="food-actions">
                <button class="action-btn calculator-btn" @click="openExerciseModal(food)">
                  <i class="el-icon-data-analysis"></i>
                  運動計算
                </button>
                <button class="action-btn favorite-btn" @click="addToFavorites(food)">
                  <i class="el-icon-star-off"></i>
                  加入最愛
                </button>
                <button class="action-btn record-btn" @click="openFoodRecordModal(food)">
                  <i class="el-icon-plus"></i>
                  加入記錄
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 推薦清單 -->
      <div v-if="!hasSearched && recommendedFoods.length > 0" class="recommended-foods">
        <h2 class="section-title">推薦清單</h2>
        <div class="food-grid">
          <div class="food-card" v-for="(food, index) in recommendedFoods" :key="index">
            <div class="food-card-content">
              <div class="food-info">
                <h3 class="food-name">{{ food.name }}</h3>
                <div class="food-details">
                  <div class="detail-item">
                    <i class="el-icon-shop"></i>
                    <span>{{ food.restaurant || '未知餐廳' }}</span>
                  </div>
                  <div class="detail-item">
                    <i class="el-icon-money"></i>
                    <span>{{ food.price }} 元</span>
                  </div>
                  <div class="detail-item">
                    <i class="el-icon-data-line"></i>
                    <span>{{ food.calories }} 大卡</span>
                  </div>
                  <div class="detail-item">
                    <i class="el-icon-food"></i>
                    <span>{{ food.food_type || '未分類' }}</span>
                  </div>
                  <div class="detail-item">
                    <i class="el-icon-menu"></i>
                    <span>{{ food.type }}</span>
                  </div>
                </div>
              </div>
              <div class="food-actions">
                <button class="action-btn calculator-btn" @click="openExerciseModal(food)">
                  <i class="el-icon-data-analysis"></i>
                  運動計算
                </button>
                <button class="action-btn favorite-btn" @click="addToFavorites(food)">
                  <i class="el-icon-star-off"></i>
                  加入最愛
                </button>
                <button class="action-btn record-btn" @click="openFoodRecordModal(food)">
                  <i class="el-icon-plus"></i>
                  加入記錄
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 無結果 -->
      <div v-if="hasSearched && searchResults.length === 0 && !isLoading" class="no-results">
        <i class="el-icon-search no-results-icon"></i>
        <p>未找到符合條件的食物</p>
      </div>

      <!-- 載入中 -->
      <div v-if="isLoading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>載入中...</p>
      </div>

      <!-- Exercise Calculator Modal -->
      <div v-if="exerciseModal" class="modal-overlay">
        <div class="modal modal-exercise">
          <div class="modal-header">
            <h3>運動計算機</h3>
            <button class="close-button" @click="closeExerciseModal">&times;</button>
          </div>
          <div class="modal-body">
            <div class="search-box">
              <input type="text" placeholder="搜尋運動" v-model="exerciseSearch" />
              <button type="button" class="search-exercise-btn">搜尋</button>
            </div>
            <div class="exercise-results">
              <div v-if="exerciseResults.running !== undefined" class="exercise-item">
                <i class="el-icon-position"></i>
                <p>跑步：<strong>{{ exerciseResults.running }}</strong> 分鐘</p>
              </div>
              <div v-if="exerciseResults.swimming !== undefined" class="exercise-item">
                <i class="el-icon-ship"></i>
                <p>游泳：<strong>{{ exerciseResults.swimming }}</strong> 分鐘</p>
              </div>
              <div v-if="exerciseResults.cycling !== undefined" class="exercise-item">
                <i class="el-icon-bicycle"></i>
                <p>騎腳踏車：<strong>{{ exerciseResults.cycling }}</strong> 分鐘</p>
              </div>
              <div v-if="exerciseResults.walking !== undefined" class="exercise-item">
                <i class="el-icon-guide"></i>
                <p>健走：<strong>{{ exerciseResults.walking }}</strong> 分鐘</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Add to Record Modal -->
      <FoodRecordModal v-model:visible="showRecordModal" :food="currentFood" @saved="onRecordSaved" />
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import FoodRecordModal from '@/components/food/FoodRecordModal.vue'

export default {
  name: 'FoodSearch',
  components: { FoodRecordModal },
  setup() {
    const router = useRouter() // 取得 router 實例

    const searchResults = ref([])
    const food_from_database = ref([])
    const recommendedFoods = ref([])
    const isLoading = ref(false)
    const hasSearched = ref(false)
    const userPreferences = ref(null)

    const filters = ref({
      priceMin: '',
      priceMax: '',
      calMin: '',
      calMax: '',
      name: '',
      restaurant: '',
      type: ''
    })

    const toggleType = (value) => {
      filters.value.type = filters.value.type === value ? '' : value
    }

    const exerciseModal = ref(false)
    const exerciseResults = ref({
      running: undefined,
      swimming: undefined,
      cycling: undefined,
      walking: undefined
    })
    const exerciseSearch = ref('')

    const showRecordModal = ref(false)
    const currentFood = ref(null)
    const openFoodRecordModal = (food) => {
      currentFood.value = food
      showRecordModal.value = true
    }
    const onRecordSaved = () => {
      // 可選：儲存後自動跳轉或刷新
      router.push({ name: 'FoodRecord' })
    }

    const handleSearch = async () => {
      const { priceMin, priceMax, calMin, calMax, name, restaurant, type } = filters.value

      const allEmpty =
        priceMin === '' &&
        priceMax === '' &&
        calMin === '' &&
        calMax === '' &&
        name.trim() === '' &&
        restaurant.trim() === '' &&
        type === ''

      if (allEmpty) return

      isLoading.value = true
      hasSearched.value = true

      try {
        // 構建API查詢參數
        const params = new URLSearchParams()
        
        if (priceMin !== '') params.append('priceMin', priceMin)
        if (priceMax !== '') params.append('priceMax', priceMax)
        if (calMin !== '') params.append('calMin', calMin)
        if (calMax !== '') params.append('calMax', calMax)
        if (name.trim() !== '') params.append('name', name.trim())
        if (restaurant.trim() !== '') params.append('restaurant', restaurant.trim())
        if (type !== '') params.append('type', type)
        
        // 發送請求到後端API
        const response = await fetch(`http://localhost:5000/api/food/?${params.toString()}`)
        
        if (!response.ok) {
          throw new Error(`API 請求失敗: ${response.status}`)
        }
        
        const data = await response.json()
        searchResults.value = data.map(item => ({
          id: item.id,
          name: item.name,
          calories: item.calories,
          price: item.price,
          type: item.type || '未分類',
          food_type: item.food_type || '未分類',
          restaurant: item.restaurant || '未知餐廳'
        }))
      } catch (error) {
        console.error('搜尋食物失敗:', error)
        ElMessage.error('搜尋食物失敗，請稍後再試')
        searchResults.value = []
      } finally {
        isLoading.value = false
      }
    }

    const addToFavorites = async (food) => {
      try {
        // 從 localStorage 獲取 userId
        const userId = localStorage.getItem('userId')
        
        if (!userId) {
          ElMessage.warning('請先登入')
          return
        }
        
        await fetch('http://localhost:5000/api/myfavorite/favorites', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user_id: parseInt(userId),
            food_id: food.id
          })
        })
        
        ElMessage.success('已添加到我的最愛')
      } catch (error) {
        console.error('添加到最愛失敗:', error)
        ElMessage.error('添加到最愛失敗，請稍後再試')
      }
    }

    //Exercise Calculator  
    const openExerciseModal = (food) => {
      exerciseModal.value = true
      calculateExercise(food.calories)
    }

    const calculateExercise = async (calories) => {
      try {
        // 呼叫後端API
        const response = await fetch(`http://localhost:5000/api/food/exercise/calculator?calories=${calories}`)
        
        if (!response.ok) {
          throw new Error(`API 請求失敗: ${response.status}`)
        }
        
        const data = await response.json()
        
        // 從API回傳的資料中提取各種運動所需的時間
        const running = data.exercises.find(e => e.type === '跑步')
        const swimming = data.exercises.find(e => e.type === '游泳')
        const cycling = data.exercises.find(e => e.type === '騎腳踏車')
        const walking = data.exercises.find(e => e.type === '健走')
        
        exerciseResults.value = {
          running: running ? running.duration : undefined,
          swimming: swimming ? swimming.duration : undefined,
          cycling: cycling ? cycling.duration : undefined,
          walking: walking ? walking.duration : undefined
        }
      } catch (error) {
        console.error('計算運動時間失敗:', error)
        ElMessage.error('無法計算運動時間，請稍後再試')
        exerciseResults.value = { running: '計算失敗', swimming: '計算失敗' }
      }
    }

    const closeExerciseModal = () => {
      exerciseModal.value = false
      exerciseResults.value = { 
        running: undefined, 
        swimming: undefined,
        cycling: undefined,
        walking: undefined
      }
      exerciseSearch.value = ''
    }

    onMounted(async () => {
      isLoading.value = true
      hasSearched.value = false // 重置搜尋狀態
      
      // 獲取用戶的偏好設置
      await loadUserPreferences()
      
      try {
        console.log('開始請求食物數據...')
        // 從後端獲取食物資料
        const apiUrl = 'http://localhost:5000/api/food/'
        console.log('請求URL:', apiUrl)
        
        const response = await fetch(apiUrl)
        
        console.log('API響應狀態:', response.status, response.statusText)
        console.log('API響應頭:', Object.fromEntries(response.headers.entries()))
        
        if (!response.ok) {
          const errorText = await response.text()
          console.error('API響應錯誤內容:', errorText)
          throw new Error(`API 請求失敗: ${response.status} ${response.statusText}`)
        }
        
        // 檢查內容類型
        const contentType = response.headers.get('content-type')
        console.log('響應內容類型:', contentType)
        
        if (!contentType || !contentType.includes('application/json')) {
          const text = await response.text()
          console.error('非JSON響應內容:', text)
          throw new Error('伺服器未返回JSON數據')
        }
        
        const data = await response.json()
        console.log('獲取到食物數據:', data)
        
        if (Array.isArray(data)) {
          // 確保數據格式一致
          food_from_database.value = data.map(item => ({
            id: item.id,
            name: item.name,
            calories: item.calories,
            price: item.price,
            type: item.type || '未分類',
            food_type: item.food_type || '未分類',
            restaurant: item.restaurant || '未知餐廳'
          }))
          // 根據用戶偏好推薦食物
          generateRecommendations()
        } else {
          console.error('回應格式不符預期:', data)
          ElMessage.warning('無法載入推薦食物，請稍後再試')
          food_from_database.value = []
          recommendedFoods.value = []
        }
      } catch (error) {
        console.error('載入食物詳細錯誤:', error)
        ElMessage.error(`無法載入食物資料: ${error.message}`)
        food_from_database.value = []
        recommendedFoods.value = []
      } finally {
        isLoading.value = false
      }
    })
    
    // 載入用戶偏好
    const loadUserPreferences = async () => {
      try {
        // 從localStorage讀取個人資料中的偏好信息
        const userId = localStorage.getItem('userId')
        
        if (!userId) {
          // 如果未登入，使用默認值
          userPreferences.value = {
            Food_Preferences: { singleDish: true, setMeal: true },
            dietaryRestrictions: {},
            spicyLevel: 1,
            priceRange: 3
          }
          return
        }
        
        // 未來可從API獲取用戶偏好，目前仍從localStorage取得
        const storedProfile = localStorage.getItem('userProfile')
        
        if (storedProfile) {
          const profileData = JSON.parse(storedProfile)
          userPreferences.value = {
            Food_Preferences: profileData.Food_Preferences || { singleDish: true, setMeal: true },
            dietaryRestrictions: profileData.dietaryRestrictions || {},
            spicyLevel: profileData.spicyLevel || 0,
            priceRange: profileData.priceRange || 3
          }
        } else {
          // 如果沒有存儲的偏好，使用默認值
          userPreferences.value = {
            Food_Preferences: { singleDish: true, setMeal: true },
            dietaryRestrictions: {},
            spicyLevel: 1,
            priceRange: 3
          }
        }
      } catch (error) {
        console.error('載入用戶偏好失敗:', error)
        // 使用默認值
        userPreferences.value = {
          Food_Preferences: { singleDish: true, setMeal: true },
          dietaryRestrictions: {},
          spicyLevel: 1,
          priceRange: 3
        }
      }
    }
    
    // 根據用戶偏好產生推薦
    const generateRecommendations = () => {
      if (!userPreferences.value || food_from_database.value.length === 0) {
        recommendedFoods.value = food_from_database.value.slice(0, 4) // 如果沒有偏好，顯示前四筆
        return
      }
      
      // 根據用戶偏好計算每個食物的適配分數
      const foodWithScores = food_from_database.value.map(food => {
        let score = 0
        
        // 價格範圍評分 (1-5分)，越接近用戶偏好價格範圍得分越高
        const priceLevel = Math.ceil((food.price || 0) / 100) // 簡單轉換，每100元一個級別
        score += 5 - Math.abs(priceLevel - userPreferences.value.priceRange)
        
        // 根據食物類型給予分數
        if (food.type === '單點') {
          score += userPreferences.value.Food_Preferences.singleDish ? 3 : 0
        } else if (food.type === '套餐') {
          score += userPreferences.value.Food_Preferences.setMeal ? 3 : 0
        }
        
        // 營養考量 (卡路里打分，假設用戶想要中等卡路里的食物，偏離中值越遠分數越低)
        const idealCalories = 500 // 中等卡路里基準值
        const caloriesDiff = Math.abs((food.calories || 0) - idealCalories)
        score += caloriesDiff < 100 ? 2 : caloriesDiff < 200 ? 1 : 0
        
        return { ...food, score }
      })
      
      // 按分數排序並取前面的項目作為推薦
      const sortedFoods = [...foodWithScores].sort((a, b) => b.score - a.score)
      recommendedFoods.value = sortedFoods.slice(0, 6) // 取前6個作為推薦
    }

    return {
      filters,
      toggleType,
      recommendedFoods,
      searchResults,
      isLoading,
      hasSearched,
      handleSearch,
      addToFavorites,
      exerciseModal,
      exerciseResults,
      exerciseSearch,
      openExerciseModal,
      calculateExercise,
      closeExerciseModal,
      showRecordModal,
      currentFood,
      openFoodRecordModal,
      onRecordSaved
    }
  }
}
</script>

<style scoped>
.food-search-page {
  padding: 20px 0;
  color: #333;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.page-title {
  margin-bottom: 24px;
  font-size: 28px;
  font-weight: 700;
  color: #333;
  text-align: center;
}

/* 搜尋表單樣式 */
.search-form-container {
  margin-bottom: 30px;
}

.search-form-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 24px;
}

.search-form-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: flex;
  gap: 20px;
}

.form-group {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-label {
  font-size: 14px;
  font-weight: 600;
  color: #666;
}

.input-with-icon {
  position: relative;
  display: flex;
  align-items: center;
}

.input-with-icon i {
  position: absolute;
  left: 12px;
  color: #aaa;
}

.form-control {
  width: 100%;
  padding: 12px 12px 12px 36px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 15px;
  transition: all 0.3s;
}

.form-control:focus {
  border-color: #ffaa55;
  box-shadow: 0 0 0 3px rgba(255, 170, 85, 0.2);
  outline: none;
}

.form-control-sm {
  padding: 8px 12px;
}

.range-inputs {
  display: flex;
  align-items: center;
  gap: 8px;
}

.range-separator {
  color: #666;
  font-weight: 600;
}

.unit {
  color: #666;
  margin-left: 4px;
}

.type-selector {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.type-buttons {
  display: flex;
  gap: 12px;
}

.type-btn {
  flex: 1;
  padding: 10px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
  color: #666;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.type-btn.active {
  background: #ffaa55;
  color: white;
  border-color: #ffaa55;
}

.type-btn:hover:not(.active) {
  background: #f5f5f5;
}

.search-btn-container {
  display: flex;
  align-items: flex-end;
}

.search-btn {
  width: 100%;
  padding: 12px;
  background: #ffaa55;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.search-btn:hover {
  background: #ff9933;
}

/* 食物卡片樣式 */
.section-title {
  font-size: 22px;
  font-weight: 700;
  margin: 30px 0 20px;
  color: #333;
  position: relative;
  padding-left: 16px;
}

.section-title::before {
  content: '';
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 6px;
  height: 24px;
  background: #ffaa55;
  border-radius: 3px;
}

.food-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.food-card {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s, box-shadow 0.3s;
}

.food-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.food-card-content {
  padding: 20px;
}

.food-name {
  font-size: 18px;
  font-weight: 700;
  margin: 0 0 16px;
  color: #333;
}

.food-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #666;
}

.detail-item i {
  color: #ffaa55;
}

.food-actions {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.action-btn {
  padding: 10px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.calculator-btn {
  background: #f0f0f0;
  color: #666;
}

.calculator-btn:hover {
  background: #e0e0e0;
}

.favorite-btn {
  background: #fff3e0;
  color: #ff9800;
}

.favorite-btn:hover {
  background: #ffe0b2;
}

.record-btn {
  background: #ffaa55;
  color: white;
}

.record-btn:hover {
  background: #ff9933;
}

/* 無結果和載入狀態 */
.no-results,
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 40px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  margin: 40px 0;
  text-align: center;
}

.no-results-icon {
  font-size: 48px;
  color: #ccc;
  margin-bottom: 16px;
}

.no-results p,
.loading-state p {
  color: #666;
  font-size: 18px;
  margin: 16px 0 0;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #ffaa55;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Modal 樣式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
}

.modal-header h3 {
  margin: 0;
  font-size: 20px;
  font-weight: 700;
  color: #333;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  color: #999;
  cursor: pointer;
  transition: color 0.3s;
}

.close-button:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
}

/* Exercise Modal 樣式 */
.search-box {
  display: flex;
  gap: 8px;
  margin-bottom: 20px;
}

.search-box input {
  flex: 1;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
}

.search-exercise-btn {
  padding: 10px 16px;
  background: #ffaa55;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.exercise-results {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.exercise-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: #f9f9f9;
  border-radius: 8px;
}

.exercise-item i {
  font-size: 24px;
  color: #ffaa55;
}

.exercise-item p {
  margin: 0;
  font-size: 16px;
}

/* 餐點類型選擇器 */
.meal-type-selector,
.quantity-selector {
  margin-bottom: 24px;
}

.meal-type-selector h4,
.quantity-selector h4 {
  margin: 0 0 12px;
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.meal-type-options {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.meal-type-option {
  position: relative;
  cursor: pointer;
}

.meal-type-option input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.meal-type-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 16px;
  background: #f5f5f5;
  border-radius: 8px;
  transition: all 0.3s;
}

.meal-type-option input:checked + .meal-type-label {
  background: #fff3e0;
  color: #ff9800;
}

.meal-type-label i {
  font-size: 24px;
}

/* 數量選擇器 */
.quantity-controls {
  display: flex;
  align-items: center;
  gap: 12px;
}

.quantity-btn {
  width: 40px;
  height: 40px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
  font-size: 18px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.quantity-btn:hover {
  background: #f5f5f5;
}

.quantity-input {
  width: 60px;
  padding: 8px;
  text-align: center;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
}

/* Modal 按鈕 */
.modal-actions {
  display: flex;
  gap: 12px;
  margin-top: 24px;
}

.modal-btn {
  flex: 1;
  padding: 12px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.cancel-btn {
  background: #f5f5f5;
  color: #666;
  border: none;
}

.cancel-btn:hover {
  background: #e0e0e0;
}

.save-btn {
  background: #ffaa55;
  color: white;
  border: none;
}

.save-btn:hover {
  background: #ff9933;
}

/* 響應式設計 */
@media (max-width: 768px) {
  .form-row {
    flex-direction: column;
    gap: 16px;
  }

  .food-grid {
    grid-template-columns: 1fr;
  }

  .meal-type-options {
    grid-template-columns: 1fr;
  }
}
</style>