<template>
  <div class="food-search-page">
    <div class="container">
      <h1 class="page-title">食物搜尋</h1>

      <!-- 搜尋表單 -->
      <div class="form-container">
        <!-- 第一欄 -->
        <div class="form-col">
          <div class="form-group">
            <label>價格</label>
            <input type="number" class="bar_short" v-model="filters.priceMin" /> ~
            <input type="number" class="bar_short" v-model="filters.priceMax" />
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
              <input type="radio" name="type" value="單點" v-model="filters.type" /> 單點
            </label>
            <label>
              <input type="radio" name="type" value="套餐" v-model="filters.type" /> 套餐
            </label>
            <button type="button" @click="handleSearch">Search</button>
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

    const handleSearch = () => {
      const {
        priceMin,
        priceMax,
        calMin,
        calMax,
        name,
        restaurant,
        type
      } = filters.value

      const allEmpty =
        priceMin === '' &&
        priceMax === '' &&
        calMin === '' &&
        calMax === '' &&
        name.trim() === '' &&
        restaurant.trim() === '' &&
        type === ''

      if (allEmpty) {
        return // 若條件全部為空，不執行搜尋
      }

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
      console.log('加入食物記錄:', food)
    }

    onMounted(() => {
      isLoading.value = true
      setTimeout(() => {
        // 推薦食物（模擬從資料庫抓取）
        recommendedFoods.value = [
          { name: '咖哩飯1', restaurant: 'CoCo壹番屋1', calories: 100, price: 190, type: '單點' },
          { name: '牛肉麵1', restaurant: '永康牛肉麵1', calories: 200, price: 180, type: '套餐' }
        ]
        // 搜尋所有食物（模擬從資料庫抓取）
        food_from_database.value = [
          { name: '咖哩飯2', restaurant: 'CoCo壹番屋2', calories: 850, price: 190, type: '單點' },
          { name: '牛肉麵2', restaurant: '永康牛肉麵2', calories: 700, price: 180, type: '套餐' }
        ]
        isLoading.value = false
      }, 500)
    })

    return {
      filters,
      recommendedFoods,
      searchResults,
      isLoading,
      hasSearched,
      handleSearch,
      addToFavorites,
      addToFoodRecord
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
</style>
