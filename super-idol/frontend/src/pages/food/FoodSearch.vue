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
              <input type="radio" name="type" value="單點" :checked="filters.type === '單點'"
              @click="toggleType('單點')" /> 單點
            </label>
            <label>
              <input type="radio" name="type" :checked="filters.type === '套餐'"
              @click="toggleType('套餐')" /> 套餐
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
              <p>餐廳: {{ food.restaurant }}</p>
              <p>熱量: {{ food.calories }} 大卡</p>
              <p>價格: {{ food.price }} 元</p>
              <p>類別: {{ food.type }} </p>
            </div>
            <div class="food-actions">
              <button @click="() => alert('Exercise Calculator')">Exercise Calculator</button>
              <button @click="addToFavorites(food)">Add to Preference</button>
              <button @click="addToFoodRecord(food)">Add to Record</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 推薦食物 -->
      <div v-if="searchResults.length === 0 && !isLoading && !hasSearched" class="recommended-foods">
        <h2 class="section-title">推薦食物</h2>
        <div class="food-grid">
          <div class="food-card" v-for="(food, index) in recommendedFoods" :key="index">
            <div class="food-info">
              <h3>{{ food.name }}</h3>
              <p>餐廳: {{ food.restaurant }}</p>
              <p>熱量: {{ food.calories }} 大卡</p>
              <p>價格: {{ food.price }} 元</p>
              <p>類別: {{ food.type }} </p>
            </div>
            <div class="food-actions">
              <button @click="() => alert('Exercise Calculator')">Exercise Calculator</button>
              <button @click="addToFavorites(food)">Add to Preference</button>
              <button @click="addToFoodRecord(food)">Add to Record</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 無結果 -->
      <div v-if="searchResults.length === 0 && hasSearched && !isLoading" class="no-results">
        <p>未找到符合條件的食物</p>
      </div>

      <!-- 載入中 -->
      <div v-if="isLoading" class="loading-state">
        <p>載入中...</p>
      </div>

      <!-- Modal -->
      <div v-if="showModal" class="modal-overlay">
        <div class="modal">
          <button class="close-button" @click="closeModal">&times;</button>
          <div class="modal-row"><strong>餐點類型</strong></div>
          <div class="modal-row">
            <label><input type="radio" value="早餐" v-model="selectedMealType" /> 早餐</label>
            <label><input type="radio" value="中餐" v-model="selectedMealType" /> 中餐</label>
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

export default {
  name: 'FoodSearch',
  setup() {
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

    const showModal = ref(false)
    const selectedMealType = ref('')
    const quantity = ref(1)
    const currentFood = ref(null)

    const handleSearch = () => {
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

      setTimeout(() => {
        const filtered = food_from_database.value.filter(food => {
          return (
            (priceMin === '' || food.price >= Number(priceMin)) &&
            (priceMax === '' || food.price <= Number(priceMax)) &&
            (calMin === '' || food.calories >= Number(calMin)) &&
            (calMax === '' || food.calories <= Number(calMax)) &&
            (name === '' || food.name.toLowerCase().includes(name.toLowerCase())) &&
            (restaurant === '' || food.restaurant.toLowerCase().includes(restaurant.toLowerCase())) &&
            (type === '' || food.type === type)
          )
        })

        searchResults.value = filtered
        isLoading.value = false
      }, 300)
    }

    const addToFavorites = (food) => {
      console.log('加入收藏:', food)
    }

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
      console.log('儲存記錄:', {
        food: currentFood.value,
        mealType: selectedMealType.value,
        quantity: quantity.value
      })
      closeModal()
    }

    onMounted(() => {
      isLoading.value = true
      setTimeout(() => {
        recommendedFoods.value = [
          { name: '漢堡1', restaurant: '麥當勞1', calories: 100, price: 190, type: '單點' },
          { name: '薯條1', restaurant: '摩斯1', calories: 200, price: 180, type: '套餐' },
          { name: '雞塊1', restaurant: 'MOS1', calories: 180, price: 60, type: '單點' },

        ]
        food_from_database.value = [
          { name: '漢堡2', restaurant: '麥當勞2', calories: 850, price: 190, type: '單點' },
          { name: '薯條2', restaurant: '摩斯2', calories: 150, price: 180, type: '套餐' },
          { name: '雞塊2', restaurant: 'MOS2', calories: 400, price: 200, type: '套餐' }
        ]
        isLoading.value = false
      }, 500)
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
</style>
