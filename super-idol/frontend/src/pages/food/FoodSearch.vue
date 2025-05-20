<template>
  <div class="food-search-page">
    <div class="container">
      <h1 class="page-title">食物搜尋</h1>

      <!-- 搜尋表單 -->
      <div class="form-container" @keydown.enter="handleSearch">
        <!-- 第一欄 -->
        <div class="form-col">
          <div class="form-group">
            <label>價格</label>
            <input type="number" class="bar_short" v-model="filters.priceMin" /> ~
            <input type="number" class="bar_short" v-model="filters.priceMax" />
            <span>元</span>
          </div>
          <div class="form-group">
            <label>熱量</label>
            <input type="number" class="bar_short" v-model="filters.calMin" /> ~
            <input type="number" class="bar_short" v-model="filters.calMax" />
            <span>大卡</span>
          </div>
        </div>

        <!-- 第二欄 -->
        <div class="form-col">
          <div class="form-group">
            <label>食物</label>
            <input type="text" class="bar_long" v-model="filters.name" />
          </div>
          <div class="form-group">
            <label>餐廳</label>
            <input type="text" class="bar_long" v-model="filters.restaurant" />
          </div>
        </div>

        <!-- 第三欄 -->
        <div class="form-col radio-col">
          <div class="form-group">
            <label>
              <input type="radio" name="type" value="單點" :checked="filters.type === '單點'" @click="toggleType('單點')" />
              單點
            </label>
            <label>
              <input type="radio" name="type" :checked="filters.type === '套餐'" @click="toggleType('套餐')" /> 套餐
            </label>
            <button type="button" @click="handleSearch">搜尋</button>
          </div>
        </div>
      </div>

      <!-- 搜尋結果 -->
      <div v-if="searchResults.length > 0" class="search-results">
        <h2 class="section-title">搜尋結果</h2>
        <div class="food-grid">
          <div class="food-card" v-for="(food, index) in searchResults" :key="index">
            <div class="food-info">
              <h3>{{ food.name }}</h3>
              <p>餐廳 : {{ food.restaurant }}</p>
              <p>價格 : {{ food.price }} 元</p>
              <p>熱量 : {{ food.calories }} 大卡</p>
              <p>類別 : {{ food.type }}</p>
            </div>
            <div class="food-actions">
              <button @click="openExerciseModal(food)">Exercise Calculator</button>
              <button @click="addToFavorites(food)">Add to Preference</button>
              <button @click="addToFoodRecord(food)">Add to Record</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 推薦清單 -->
      <div v-if="!hasSearched && recommendedFoods.length > 0" class="recommended-foods">
        <h2 class="section-title">推薦清單</h2>
        <div class="food-grid">
          <div class="food-card" v-for="(food, index) in recommendedFoods" :key="index">
            <div class="food-info">
              <h3>{{ food.name }}</h3>
              <p>餐廳 : {{ food.restaurant }}</p>
              <p>價格 : {{ food.price }} 元</p>
              <p>熱量 : {{ food.calories }} 大卡</p>
              <p>類別 : {{ food.type }}</p>
            </div>
            <div class="food-actions">
              <button @click="openExerciseModal(food)">Exercise Calculator</button>
              <button @click="addToFavorites(food)">Add to Preference</button>
              <button @click="addToFoodRecord(food)">Add to Record</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 無結果 -->
      <div v-if="hasSearched && searchResults.length === 0 && !isLoading" class="no-results">
        <p>未找到符合條件的食物</p>
      </div>

      <!-- 載入中 -->
      <div v-if="isLoading" class="loading-state">
        <p>載入中...</p>
      </div>

      <!-- Exercise Calculator Modal -->
      <div v-if="exerciseModal" class="modal-overlay">
        <div class="modal">
          <button class="close-button" @click="closeExerciseModal">&times;</button>
          <div class="modal-row"><strong>運動計算機</strong></div>
          <div class="modal-row">
            <input type="text" placeholder="搜尋運動" v-model="exerciseSearch" />
            <button type="button" >搜尋</button>
          </div>
          <div class="modal-row">
            <p>跑步：{{ exerciseResults.running }} 分鐘</p>
          </div>
          <div class="modal-row">
            <p>游泳：{{ exerciseResults.swimming }} 分鐘</p>
          </div>
        </div>
      </div>

      <!-- Add to Record Modal -->
      <div v-if="showModal" class="modal-overlay">
        <div class="modal">
          <button class="close-button" @click="closeModal">&times;</button>
          <div class="modal-row"><strong>餐點類型</strong></div>
          <div class="modal-row">
            <label><input type="radio" value="早餐" v-model="selectedMealType" /> 早餐</label>
            <label><input type="radio" value="午餐" v-model="selectedMealType" /> 午餐</label>
            <label><input type="radio" value="晚餐" v-model="selectedMealType" /> 晚餐</label>
            <label><input type="radio" value="點心" v-model="selectedMealType" /> 點心</label>
          </div>
          <div class="modal-row">
            <label>選擇數量</label>
            <input type="number" v-model="quantity" min="1" />
          </div>
          <div class="modal-row">
            <button @click="closeModal">Cancel</button>
            <button @click="saveRecord">Save</button>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'FoodSearch',
  setup() {
    const router = useRouter() // 取得 router 實例

    const searchResults = ref([])
    const food_from_database = ref([])
    const recommendedFoods = ref([])
    const isLoading = ref(false)
    const hasSearched = ref(false)

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
      running: '',
      swimming: ''
    })
    const exerciseSearch = ref('')


    const showModal = ref(false)
    const selectedMealType = ref('')
    const quantity = ref(1)
    const currentFood = ref(null)

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

      if (allEmpty) {
        // 如果沒有搜尋條件，顯示所有食物
        searchResults.value = food_from_database.value
        return
      }

      isLoading.value = true
      hasSearched.value = true

      try {
        // 構建查詢參數
        const queryParams = new URLSearchParams()
        if (priceMin) queryParams.append('priceMin', priceMin)
        if (priceMax) queryParams.append('priceMax', priceMax)
        if (calMin) queryParams.append('calMin', calMin)
        if (calMax) queryParams.append('calMax', calMax)
        if (name.trim()) queryParams.append('name', name.trim())
        if (restaurant.trim()) queryParams.append('restaurant', restaurant.trim())
        if (type) queryParams.append('type', type)

        // 發送搜尋請求到後端
        const response = await fetch(`http://localhost:5000/food/?${queryParams.toString()}`)
        const data = await response.json()
        
        if (Array.isArray(data)) {
          searchResults.value = data
        } else {
          console.error('Unexpected response format:', data)
          searchResults.value = []
        }
      } catch (error) {
        console.error('搜尋食物失敗:', error)
        searchResults.value = []
      } finally {
        isLoading.value = false
      }
    }

    const addToFavorites = (food) => {
      console.log('加入收藏:', food)
    }

    //Exercise Calculator   
    const openExerciseModal = (food) => {
      exerciseModal.value = true
      calculateExercise(food.calories)
    }

    const calculateExercise = (calories) => {
      // 假裝呼叫後端
      setTimeout(() => {
        exerciseResults.value.running = Math.ceil(calories / 10) // 跑步10大卡/分鐘
        exerciseResults.value.swimming = Math.ceil(calories / 8) // 游泳8大卡/分鐘
      }, 300)
    }

    const closeExerciseModal = () => {
      exerciseModal.value = false
      exerciseResults.value = { running: '', swimming: '' }
      exerciseSearch.value = ''
    }

    //Add to Record
    const addToFoodRecord = (food) => {
      currentFood.value = food
      showModal.value = true
    }

    const closeModal = () => {
      showModal.value = false
      selectedMealType.value = ''
      quantity.value = 1
      currentFood.value = null
    }

    const saveRecord = () => {
      if (!selectedMealType.value) {
        alert('請選擇餐點類型')
        return
      }
      // 組合要傳的參數
      const foodData = {
        name: currentFood.value.name,
        restaurant: currentFood.value.restaurant,
        calories: currentFood.value.calories,
        price: currentFood.value.price,
        type: currentFood.value.type,
        mealType: selectedMealType.value,
        quantity: quantity.value
      }

      // 跳轉到 FoodRecord 頁面並帶參數
      router.push({
        name: 'FoodRecord', // 請確認路由名稱
        query: foodData
      })

      closeModal()
    }

    onMounted(async () => {
      isLoading.value = true
      hasSearched.value = false // 重置搜尋狀態
      
      try {
        // 從後端獲取食物資料
        const response = await fetch('http://localhost:5000/food/')
        const data = await response.json()
        
        if (Array.isArray(data)) {
          food_from_database.value = data
          // 確保有資料時才設定推薦清單
          if (data.length > 0) {
            recommendedFoods.value = data.slice(0, 4) // 顯示前四筆作為推薦
          } else {
            console.log('沒有找到任何食物資料')
            recommendedFoods.value = []
          }
        } else {
          console.error('Unexpected response format:', data)
          recommendedFoods.value = []
        }
      } catch (error) {
        console.error('載入食物失敗:', error)
        recommendedFoods.value = []
      } finally {
        isLoading.value = false
      }
    })

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
      addToFoodRecord,
      showModal,
      selectedMealType,
      quantity,
      currentFood,
      closeModal,
      saveRecord
    }
  }
}
</script>

<style scoped>
.food-search-page {
  padding: 20px 0;
}

.page-title {
  margin-bottom: 24px;
  font-size: 28px;
  color: var(--text-color);
}

.form-container {
  display: flex;
  align-items: flex-start;
  gap: 50px;
  margin-bottom: 24px;
}

.form-col {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.radio-col {
  margin-top: 4px;
}

.form-group {
  display: flex;
  align-items: center;
  gap: 8px;
}

.form-group button {
  background-color: rgb(255, 192, 76);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 5px 13px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.form-group button:hover {
  background-color: orange;
}


.bar_short {
  border-radius: 5px;
  width: 8dvb;
}

.bar_long {
  border-radius: 5px;
}

.section-title {
  font-size: 20px;
  margin: 16px 0;
  color: var(--text-color);
}

.food-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
  margin-bottom: 32px;
}

.food-card {
  background: #fff;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.food-info {
  flex: 1;
}

.food-actions {
  display: flex;
  flex-direction: column;
  gap: 4px;
  justify-content: center;
}

.food-actions button {
  background-color: #ffeb85;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.food-actions button:hover {
  background-color: rgb(255, 192, 76);
}


.no-results,
.loading-state {
  display: flex;
  justify-content: center;
  padding: 40px;
  background-color: var(--card-bg);
  border-radius: 8px;
  margin-top: 24px;
}

.no-results p,
.loading-state p {
  color: #666;
  font-size: 18px;
}

.modal {
  position: fixed;
  top: 20px;
  right: 20px;
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  max-width: 300px;
}

.modal-content {
  position: relative;
}

.close-button {
  position: absolute;
  top: 4px;
  right: 8px;
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal {
  background: #fff;
  padding: 24px;
  border-radius: 8px;
  width: 400px;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.close-button {
  position: absolute;
  top: 8px;
  right: 8px;
  border: none;
  background: transparent;
  font-size: 20px;
  color: red;
  cursor: pointer;
}

.modal-row {
  display: flex;
  gap: 12px;
  align-items: center;
  flex-wrap: wrap;
}

.modal-row button {
  background-color: #ffeb85;
  /* 鵝黃色 */
  color: #333;
  border: none;
  border-radius: 20px;
  padding: 8px 20px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.modal-row button:hover {
  background-color: #f5d94b;
  /* 深一點的鵝黃色 */
}
</style>