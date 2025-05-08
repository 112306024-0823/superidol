<template>
  <div class="my-favorite-page">
    <div class="container">
      <h1 class="page-title">我的最愛</h1>
      
      <!-- 收藏的食物列表 -->
      <div class="favorite-foods-container">
        <!-- 使用現有的 FoodCard 組件顯示收藏食物 -->
        <!-- TODO: 实现收藏食物列表，使用 v-for 遍历收藏的食物数据 -->
      </div>
      
      <!-- 空狀態顯示 -->
      <div v-if="!favoriteFoods.length" class="empty-state">
        <p>您還沒有收藏任何食物</p>
        <router-link to="/food/search" class="btn btn-primary">
          瀏覽食物
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
// TODO: 導入 FoodCard 組件
// import FoodCard from '../../components/food/FoodCard.vue'

export default {
  name: 'MyFavorite',
  components: {
    // FoodCard
  },
  setup() {
    // 收藏的食物
    const favoriteFoods = ref([])
    const isLoading = ref(false)
    
    // 載入收藏食物
    onMounted(async () => {
      isLoading.value = true
      try {
        // TODO: 從API獲取用戶收藏的食物
        // 模擬數據
        favoriteFoods.value = [
          // 示例數據
        ]
      } catch (error) {
        console.error('獲取收藏失敗:', error)
      } finally {
        isLoading.value = false
      }
    })
    
    // 移除收藏
    const removeFromFavorites = async (foodId) => {
      // TODO: 呼叫API移除收藏
      console.log('移除收藏:', foodId)
    }
    
    // 添加到食物記錄
    const addToFoodRecord = (food) => {
      // TODO: 導航到添加食物記錄頁面，並傳遞選擇的食物
      console.log('添加到食物記錄:', food)
    }
    
    return {
      favoriteFoods,
      isLoading,
      removeFromFavorites,
      addToFoodRecord
    }
  }
}
</script>

<style scoped>
.my-favorite-page {
  padding: 20px 0;
}

.page-title {
  margin-bottom: 24px;
  font-size: 28px;
  color: var(--text-color);
}

.favorite-foods-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  background-color: var(--card-bg);
  border-radius: 8px;
  text-align: center;
}

.empty-state p {
  margin-bottom: 16px;
  color: #666;
  font-size: 18px;
}
</style> 