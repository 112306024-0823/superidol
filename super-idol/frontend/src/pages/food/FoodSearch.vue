<template>
  <div class="food-search-page">
    <div class="container">
      <h1 class="page-title">食物搜尋</h1>
      
      <!-- 搜尋欄 -->
      <div class="search-bar">
        <input 
          type="text" 
          v-model="searchQuery" 
          @input="handleSearch"
          class="search-input" 
          placeholder="搜尋食物..."
        />
        <button class="btn btn-primary search-btn" @click="handleSearch">
          搜尋
        </button>
      </div>
      
      <!-- 搜尋結果 -->
      <div v-if="searchQuery && searchResults.length > 0" class="search-results">
        <h2 class="section-title">搜尋結果</h2>
        <div class="food-grid">
          <!-- TODO: 使用 FoodCard 組件顯示搜尋結果 -->
          <!-- 使用 v-for 遍歷搜尋結果 -->
        </div>
      </div>
      
      <!-- 推薦食物 (當沒有搜尋查詢時顯示) -->
      <div v-if="!searchQuery" class="recommended-foods">
        <h2 class="section-title">推薦食物</h2>
        <div class="food-grid">
          <!-- TODO: 使用 FoodCard 組件顯示推薦食物 -->
          <!-- 使用 v-for 遍歷推薦食物列表 -->
        </div>
      </div>
      
      <!-- 搜尋無結果 -->
      <div v-if="searchQuery && searchResults.length === 0 && !isLoading" class="no-results">
        <p>未找到與 "{{ searchQuery }}" 相符的食物</p>
      </div>
      
      <!-- 載入中狀態 -->
      <div v-if="isLoading" class="loading-state">
        <p>載入中...</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, watch, onMounted } from 'vue'
// TODO: 導入 FoodCard 組件及 food store
// import FoodCard from '../../components/food/FoodCard.vue'
// import { useFoodStore } from '../../store/food'

export default {
  name: 'FoodSearch',
  components: {
    // FoodCard
  },
  setup() {
    // const foodStore = useFoodStore()
    
    const searchQuery = ref('')
    const searchResults = ref([])
    const recommendedFoods = ref([])
    const isLoading = ref(false)
    
    // 處理搜尋
    const handleSearch = async () => {
      if (!searchQuery.value.trim()) {
        searchResults.value = []
        return
      }
      
      isLoading.value = true
      try {
        // TODO: 使用 store 或 API 搜尋食物
        // searchResults.value = await foodStore.searchFood(searchQuery.value)
        
        // 模擬搜尋結果
        await new Promise(resolve => setTimeout(resolve, 500))
        searchResults.value = [
          // 示例搜尋結果數據
        ]
      } catch (error) {
        console.error('搜尋失敗:', error)
      } finally {
        isLoading.value = false
      }
    }
    
    // 添加到收藏
    const addToFavorites = async (food) => {
      // TODO: 實現添加到收藏功能
      console.log('添加到收藏:', food)
    }
    
    // 添加到食物記錄
    const addToFoodRecord = (food) => {
      // TODO: 導航到添加食物記錄頁面，並傳遞選擇的食物
      console.log('添加到食物記錄:', food)
    }
    
    // 獲取推薦食物
    onMounted(async () => {
      isLoading.value = true
      try {
        // TODO: 從API獲取推薦食物
        // 模擬數據
        await new Promise(resolve => setTimeout(resolve, 500))
        recommendedFoods.value = [
          // 示例推薦食物數據
        ]
      } catch (error) {
        console.error('獲取推薦食物失敗:', error)
      } finally {
        isLoading.value = false
      }
    })
    
    return {
      searchQuery,
      searchResults,
      recommendedFoods,
      isLoading,
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

.search-bar {
  display: flex;
  margin-bottom: 24px;
}

.search-input {
  flex: 1;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px 0 0 4px;
  font-size: 16px;
}

.search-btn {
  border-radius: 0 4px 4px 0;
}

.section-title {
  font-size: 20px;
  margin: 16px 0;
  color: var(--text-color);
}

.food-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.no-results, .loading-state {
  display: flex;
  justify-content: center;
  padding: 40px;
  background-color: var(--card-bg);
  border-radius: 8px;
  margin-top: 24px;
}

.no-results p, .loading-state p {
  color: #666;
  font-size: 18px;
}
</style> 