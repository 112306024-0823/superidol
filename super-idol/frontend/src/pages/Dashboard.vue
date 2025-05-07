<template>
  <div class="dashboard">
    <div class="container">
      <h1 class="page-title">儀表板</h1>
      
      <div class="welcome-card card">
        <h2>歡迎回來，{{ user.name }}</h2>
        <p>今天是 {{ currentDate }}，這是您的健康飲食摘要</p>
      </div>
      
      <div class="dashboard-grid">
        <!-- 卡路里摘要卡片 -->
        <div class="card dashboard-card">
          <h3>今日熱量</h3>
          <div class="card-content">
            <div class="calorie-info">
              <div class="calorie-consumed">
                <span class="value">{{ todaySummary.caloriesConsumed }}</span>
                <span class="label">已攝取</span>
              </div>
              <div class="calorie-target">
                <span class="value">{{ userGoals.dailyCalories }}</span>
                <span class="label">目標</span>
              </div>
              <div class="calorie-remaining">
                <span class="value">{{ caloriesRemaining }}</span>
                <span class="label">剩餘</span>
              </div>
            </div>
            <div class="progress-container">
              <div 
                class="progress-bar" 
                :style="{ width: calorieProgressPercentage + '%' }"
                :class="{ 'exceed': calorieProgressPercentage > 100 }"
              ></div>
            </div>
          </div>
        </div>
        
        <!-- 營養素摘要卡片 -->
        <div class="card dashboard-card">
          <h3>營養素攝取</h3>
          <div class="card-content">
            <div class="nutrient-grid">
              <div class="nutrient-item">
                <span class="nutrient-value">{{ todaySummary.protein }}g</span>
                <span class="nutrient-label">蛋白質</span>
              </div>
              <div class="nutrient-item">
                <span class="nutrient-value">{{ todaySummary.carbs }}g</span>
                <span class="nutrient-label">碳水化合物</span>
              </div>
              <div class="nutrient-item">
                <span class="nutrient-value">{{ todaySummary.fat }}g</span>
                <span class="nutrient-label">脂肪</span>
              </div>
              <div class="nutrient-item">
                <span class="nutrient-value">{{ todaySummary.sugar }}g</span>
                <span class="nutrient-label">糖</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 最近食物記錄卡片 -->
        <div class="card dashboard-card">
          <h3>最近食物記錄</h3>
          <div class="card-content">
            <div v-if="recentFoods.length > 0" class="recent-food-list">
              <div v-for="food in recentFoods" :key="food.id" class="recent-food-item">
                <div class="food-info">
                  <span class="food-name">{{ food.name }}</span>
                  <span class="food-calories">{{ food.calories }} 卡路里</span>
                </div>
                <span class="food-time">{{ formatTime(food.timestamp) }}</span>
              </div>
            </div>
            <div v-else class="empty-state">
              <p>今天還沒有食物記錄</p>
              <router-link to="/food/search" class="btn btn-primary">添加食物</router-link>
            </div>
          </div>
        </div>
        
        <!-- 運動記錄卡片 -->
        <div class="card dashboard-card">
          <h3>今日運動</h3>
          <div class="card-content">
            <div v-if="todayExercises.length > 0" class="exercise-list">
              <div v-for="exercise in todayExercises" :key="exercise.id" class="exercise-item">
                <div class="exercise-info">
                  <span class="exercise-name">{{ exercise.name }}</span>
                  <span class="exercise-duration">{{ exercise.duration }} 分鐘</span>
                </div>
                <span class="exercise-calories">-{{ exercise.caloriesBurned }} 卡路里</span>
              </div>
            </div>
            <div v-else class="empty-state">
              <p>今天還沒有運動記錄</p>
              <router-link to="/exercise/log" class="btn btn-primary">記錄運動</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue'
import { useAuthStore } from '../store/auth'
// 根據需要導入其他 store

export default {
  name: 'Dashboard',
  setup() {
    const authStore = useAuthStore()
    const user = computed(() => authStore.user || {})
    
    // 範例資料，實際應用中應該從 API 或 store 獲取
    const userGoals = ref({
      dailyCalories: 2000,
      protein: 150,
      carbs: 200,
      fat: 65
    })
    
    const todaySummary = ref({
      caloriesConsumed: 1250,
      protein: 85,
      carbs: 120,
      fat: 45,
      sugar: 30
    })
    
    const recentFoods = ref([
      { id: 1, name: '牛肉漢堡', calories: 450, timestamp: new Date(Date.now() - 3600000) },
      { id: 2, name: '凱薩沙拉', calories: 320, timestamp: new Date(Date.now() - 7200000) },
      { id: 3, name: '水果優格', calories: 180, timestamp: new Date(Date.now() - 10800000) }
    ])
    
    const todayExercises = ref([
      { id: 1, name: '跑步', duration: 30, caloriesBurned: 300 },
      { id: 2, name: '健身房重訓', duration: 45, caloriesBurned: 250 }
    ])
    
    // 計算剩餘卡路里
    const caloriesRemaining = computed(() => {
      return userGoals.value.dailyCalories - todaySummary.value.caloriesConsumed
    })
    
    // 計算卡路里進度百分比
    const calorieProgressPercentage = computed(() => {
      return (todaySummary.value.caloriesConsumed / userGoals.value.dailyCalories) * 100
    })
    
    // 格式化日期
    const currentDate = computed(() => {
      const options = { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' }
      return new Date().toLocaleDateString('zh-TW', options)
    })
    
    // 格式化時間
    const formatTime = (timestamp) => {
      return new Date(timestamp).toLocaleTimeString('zh-TW', { hour: '2-digit', minute: '2-digit' })
    }
    
    onMounted(() => {
      // 在組件掛載時加載數據
      // loadUserData()
      // loadTodaySummary()
      // loadRecentFoods()
      // loadTodayExercises()
    })
    
    return {
      user,
      userGoals,
      todaySummary,
      recentFoods,
      todayExercises,
      caloriesRemaining,
      calorieProgressPercentage,
      currentDate,
      formatTime
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding-top: 20px;
}

.page-title {
  margin-bottom: 24px;
  font-size: 28px;
  color: var(--text-color);
}

.welcome-card {
  margin-bottom: 24px;
  padding: 20px;
}

.welcome-card h2 {
  font-size: 24px;
  margin-bottom: 8px;
  color: var(--primary-color);
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-gap: 20px;
}

.dashboard-card {
  height: 100%;
}

.dashboard-card h3 {
  padding: 16px;
  margin: 0;
  border-bottom: 1px solid var(--border-color);
  font-size: 18px;
}

.card-content {
  padding: 16px;
}

/* 卡路里卡片樣式 */
.calorie-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 16px;
}

.calorie-consumed,
.calorie-target,
.calorie-remaining {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.value {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 4px;
}

.label {
  font-size: 14px;
  color: #666;
}

.progress-container {
  height: 8px;
  background-color: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background-color: var(--primary-color);
  transition: width 0.3s ease;
}

.progress-bar.exceed {
  background-color: var(--danger-color);
}

/* 營養素樣式 */
.nutrient-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-gap: 16px;
}

.nutrient-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px;
  background-color: rgba(0, 0, 0, 0.03);
  border-radius: 8px;
}

.nutrient-value {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 4px;
}

.nutrient-label {
  font-size: 14px;
  color: #666;
}

/* 食物列表樣式 */
.recent-food-item,
.exercise-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #eee;
}

.recent-food-item:last-child,
.exercise-item:last-child {
  border-bottom: none;
}

.food-info,
.exercise-info {
  display: flex;
  flex-direction: column;
}

.food-name,
.exercise-name {
  font-weight: 500;
  margin-bottom: 4px;
}

.food-calories,
.exercise-duration,
.exercise-calories {
  font-size: 14px;
  color: #666;
}

.exercise-calories {
  color: var(--success-color);
  font-weight: 500;
}

.food-time {
  font-size: 14px;
  color: #888;
}

/* 空狀態 */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 24px 0;
}

.empty-state p {
  margin-bottom: 16px;
  color: #666;
}

@media (max-width: 768px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}
</style> 