<template>
  <div class="food-record-page">
    <div class="container">
      <h1 class="page-title">食物記錄</h1>
      
      <!-- 日期選擇器 -->
      <div class="date-selector">
        <button class="btn btn-icon" @click="changeDate(-1)">
          <i class="icon-left-arrow"></i>
        </button>
        <h2 class="current-date">{{ formattedDate }}</h2>
        <button class="btn btn-icon" @click="changeDate(1)">
          <i class="icon-right-arrow"></i>
        </button>
      </div>
      
      <!-- 每日卡路里摘要 -->
      <div class="calorie-summary">
        <div class="calorie-info">
          <div class="calorie-consumed">
            <span class="value">{{ dailySummary.calories }}</span>
            <span class="label">已攝取</span>
          </div>
          <div class="calorie-target">
            <span class="value">{{ calorieGoal }}</span>
            <span class="label">目標</span>
          </div>
          <div class="calorie-remaining">
            <span class="value">{{ calorieRemaining }}</span>
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
      
      <!-- 餐點記錄 -->
      <div class="food-record-container">
        <!-- 早餐 -->
        <div class="meal-section">
          <div class="meal-header">
            <h3 class="meal-title">早餐</h3>
            <button class="btn btn-sm btn-primary add-food-btn" @click="addFood('breakfast')">添加食物</button>

          </div>
          
          <div class="meal-items">
            <!-- TODO: 使用 v-for 遍歷早餐食物列表 -->
            <div v-if="!breakfastItems.length" class="empty-meal">
              <p>尚未添加早餐食物</p>
            </div>
          </div>
        </div>
        
        <!-- 午餐 -->
        <div class="meal-section">
          <div class="meal-header">
            <h3 class="meal-title">午餐</h3>
            <button class="btn btn-sm btn-primary add-food-btn" @click="addFood('lunch')">添加食物</button>
          </div>
          
          <div class="meal-items">
            <!-- TODO: 使用 v-for 遍歷午餐食物列表 -->
            <div v-if="!lunchItems.length" class="empty-meal">
              <p>尚未添加午餐食物</p>
            </div>
          </div>
        </div>
        
        <!-- 晚餐 -->
        <div class="meal-section">
          <div class="meal-header">
            <h3 class="meal-title">晚餐</h3>
            <button class="btn btn-sm btn-primary add-food-btn" @click="addFood('dinner')">添加食物</button>
          </div>
          
          <div class="meal-items">
            <!-- TODO: 使用 v-for 遍歷晚餐食物列表 -->
            <div v-if="!dinnerItems.length" class="empty-meal">
              <p>尚未添加晚餐食物</p>
            </div>
          </div>
        </div>
        
        <!-- 點心 -->
        <div class="meal-section">
          <div class="meal-header">
            <h3 class="meal-title">點心</h3>
            <button class="btn btn-sm btn-primary add-food-btn" @click="addFood('snacks')">添加食物</button>

          </div>
          
          <div class="meal-items">
            <!-- TODO: 使用 v-for 遍歷點心食物列表 -->
            <div v-if="!snackItems.length" class="empty-meal">
              <p>尚未添加點心食物</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 添加食物彈窗 (後續實現) -->
    <!-- TODO: 實現添加食物彈窗 -->
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
// TODO: 導入相關 store 和工具函數
// import { useFoodStore } from '../../store/food'
// import { formatDate } from '../../utils/date'

export default {
  name: 'FoodRecord',
  setup() {
    // const foodStore = useFoodStore()
    const router = useRouter()
    
    // 當前選中的日期
    const selectedDate = ref(new Date())
    
    // 卡路里目標 (實際應從用戶設置獲取)
    const calorieGoal = ref(2000)
    
    // 模擬各餐食物數據
    const breakfastItems = ref([])
    const lunchItems = ref([])
    const dinnerItems = ref([])
    const snackItems = ref([])
    
    // 格式化日期
    const formattedDate = computed(() => {
      return selectedDate.value.toLocaleDateString('zh-TW', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
      })
    })
    
    // 計算每日摘要
    const dailySummary = computed(() => {
      // TODO: 實際實現中應計算所有餐點的總和
      return {
        calories: 1250,
        protein: 85,
        carbs: 120,
        fat: 45
      }
    })
    
    // 計算剩餘卡路里
    const calorieRemaining = computed(() => {
      return calorieGoal.value - dailySummary.value.calories
    })
    
    // 計算卡路里進度百分比
    const calorieProgressPercentage = computed(() => {
      return (dailySummary.value.calories / calorieGoal.value) * 100
    })
    
    // 更改日期
    const changeDate = (days) => {
      const newDate = new Date(selectedDate.value)
      newDate.setDate(newDate.getDate() + days)
      selectedDate.value = newDate
      
      // TODO: 加載所選日期的食物記錄
      loadFoodRecords()
    }
    
    // 加載食物記錄
    const loadFoodRecords = async () => {
      // TODO: 從API獲取所選日期的食物記錄
      console.log('加載日期', selectedDate.value, '的食物記錄')
      
      // 模擬數據
      breakfastItems.value = []
      lunchItems.value = []
      dinnerItems.value = []
      snackItems.value = []
    }
    
    // 添加食物到指定餐點
    const addFood = (mealType) => {
      // TODO: 導航到食物搜尋頁面或打開食物選擇彈窗
      router.push({
        path: '/food/search',
        query: { 
          returnTo: '/food/record',
          mealType: mealType,
          date: selectedDate.value.toISOString().split('T')[0] 
        }
      })
    }
    
    // 刪除食物記錄
    const deleteRecord = async (recordId) => {
      // TODO: 實現刪除食物記錄功能
      console.log('刪除記錄', recordId)
    }
    
    // 初始化
    onMounted(() => {
      loadFoodRecords()
    })
    
    return {
      selectedDate,
      formattedDate,
      calorieGoal,
      dailySummary,
      calorieRemaining,
      calorieProgressPercentage,
      breakfastItems,
      lunchItems,
      dinnerItems,
      snackItems,
      changeDate,
      addFood,
      deleteRecord
    }
  }
}
</script>

<style scoped>
.food-record-page {
  padding: 20px 0;
}

.page-title {
  margin-bottom: 24px;
  font-size: 28px;
  color: var(--text-color);
}

.date-selector {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
}

.current-date {
  margin: 0 16px;
  font-size: 20px;
  color: var(--text-color);
}

.btn-icon {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: var(--primary-color);
}

.calorie-summary {
  background-color: var(--card-bg);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

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

.food-record-container {
  background-color: var(--card-bg);
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.meal-section {
  border-bottom: 1px solid #eee;
  padding: 16px;
}

.meal-section:last-child {
  border-bottom: none;
}

.meal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.meal-title {
  font-size: 18px;
  margin: 0;
  color: var(--text-color);
}

.empty-meal {
  padding: 12px;
  text-align: center;
  color: #888;
  background-color: rgba(0, 0, 0, 0.02);
  border-radius: 4px;
}

.meal-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.add-food-btn {
  background-color: #ffa940;
  color: white;
  border: 1px solid #ffa940;
  border-radius: 24px;      /* 大圓角，圓弧效果 */
  padding: 6px 20px;        /* 上下內距6px，左右20px */
  font-weight: 600;
  transition: background-color 0.3s ease;
  cursor: pointer;
}

.add-food-btn:hover {
  background-color: #d48806;
  border-color: #d48806;
  color: white;
}


@media (max-width: 768px) {
  .calorie-info {
    flex-wrap: wrap;
  }
  
  .calorie-consumed,
  .calorie-target,
  .calorie-remaining {
    flex: 1;
    min-width: 30%;
    margin-bottom: 12px;
  }
}
</style> 