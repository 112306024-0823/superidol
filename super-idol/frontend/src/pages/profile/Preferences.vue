<template>
  <div class="preference-page">
    <div class="container">
      <h1 class="page-title">我的收藏</h1>

      <!-- 載入中狀態 -->
      <div v-if="isLoading" class="loading-state">
        <div class="loading-spinner"></div>
        <p>載入中...</p>
      </div>

      <!-- 無收藏提示 -->
      <div v-if="!isLoading && favorites.length === 0" class="no-results">
        <i class="el-icon-star-off no-results-icon"></i>
        <p>尚未收藏任何食物</p>
        <p class="no-results-subtitle">到食物搜尋頁面尋找喜歡的食物並加入收藏吧！</p>
      </div>

      <!-- 收藏列表 -->
      <div v-if="favorites.length > 0" class="favorites-section">
        <div class="favorites-count">
          <p>共 {{ favorites.length }} 項收藏</p>
        </div>
        <div class="food-grid">
          <div class="food-card" v-for="(food, index) in favorites" :key="food.id">
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
                <button class="action-btn remove-btn" @click="confirmRemoveFavorite(food)" :disabled="isRemoving">
                  <i class="el-icon-star-off"></i>
                  {{ isRemoving ? '移除中...' : '移除收藏' }}
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 確認刪除 Modal -->
      <div v-if="showConfirmModal" class="modal-overlay">
        <div class="modal">
          <div class="modal-header">
            <h3>確認移除收藏</h3>
          </div>
          <div class="modal-body">
            <p>確定要移除 <strong>{{ selectedFood?.name }}</strong> 的收藏嗎？</p>
          </div>
          <div class="modal-actions">
            <button class="modal-btn cancel-btn" @click="cancelRemove">取消</button>
            <button class="modal-btn confirm-btn" @click="removeFavorite" :disabled="isRemoving">
              {{ isRemoving ? '移除中...' : '確認移除' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'Preference',
  setup() {
    const favorites = ref([])
    const isLoading = ref(false)
    const isRemoving = ref(false)
    const showConfirmModal = ref(false)
    const selectedFood = ref(null)

    // 載入收藏資料
    const fetchFavorites = async () => {
      const userId = localStorage.getItem('userId')
      if (!userId) {
        ElMessage.warning('請先登入')
        return
      }

      isLoading.value = true
      try {
        console.log('開始載入收藏資料，userId:', userId)
        
        const response = await fetch(`http://localhost:5000/api/food/favorites?user_id=${userId}`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          }
        })
        
        console.log('API 回應狀態:', response.status)
        
        if (!response.ok) {
          const errorText = await response.text()
          console.error('API 錯誤回應:', errorText)
          throw new Error(`HTTP ${response.status}: ${response.statusText}`)
        }

        const data = await response.json()
        console.log('獲取到的收藏資料:', data)
        
        // 確保資料格式正確
        if (Array.isArray(data)) {
          favorites.value = data.map(item => ({
            id: item.id,
            name: item.name || '未知食物',
            calories: item.calories || 0,
            price: item.price || 0,
            type: item.type || '未分類',
            food_type: item.food_type || '未分類',
            restaurant: item.restaurant || '未知餐廳'
          }))
          
          console.log('處理後的收藏資料:', favorites.value)
          
          if (favorites.value.length > 0) {
            ElMessage.success(`載入了 ${favorites.value.length} 項收藏`)
          }
        } else {
          console.warn('API 回傳的不是陣列格式:', data)
          throw new Error('API 回傳資料格式錯誤')
        }
        
      } catch (error) {
        console.error('載入收藏失敗:', error)
        ElMessage.error(`載入收藏失敗: ${error.message}`)
        favorites.value = []
      } finally {
        isLoading.value = false
      }
    }

    // 確認移除收藏
    const confirmRemoveFavorite = (food) => {
      selectedFood.value = food
      showConfirmModal.value = true
    }

    // 取消移除
    const cancelRemove = () => {
      showConfirmModal.value = false
      selectedFood.value = null
    }

    // 刪除收藏
    const removeFavorite = async () => {
      if (!selectedFood.value) return

      const userId = localStorage.getItem('userId')
      if (!userId) {
        ElMessage.warning('請先登入')
        return
      }

      isRemoving.value = true
      try {
        console.log('準備移除收藏，食物ID:', selectedFood.value.id)
        
        const response = await fetch('http://localhost:5000/api/food/favorites', {
          method: 'DELETE',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user_id: parseInt(userId),
            food_id: selectedFood.value.id
          }),
        })
        
        console.log('刪除API回應狀態:', response.status)
        
        if (!response.ok) {
          const errorText = await response.text()
          console.error('刪除API錯誤:', errorText)
          throw new Error(`刪除失敗: HTTP ${response.status}`)
        }

        const result = await response.json()
        console.log('刪除結果:', result)

        ElMessage.success('已移除收藏')
        
        // 從列表中移除該項目
        favorites.value = favorites.value.filter(food => food.id !== selectedFood.value.id)
        
        // 關閉 modal
        showConfirmModal.value = false
        selectedFood.value = null
        
      } catch (error) {
        console.error('移除收藏失敗:', error)
        ElMessage.error(`移除收藏失敗: ${error.message}`)
      } finally {
        isRemoving.value = false
      }
    }

    onMounted(() => {
      console.log('Preference 組件已掛載，開始載入收藏')
      fetchFavorites()
    })

    return {
      favorites,
      isLoading,
      isRemoving,
      showConfirmModal,
      selectedFood,
      confirmRemoveFavorite,
      cancelRemove,
      removeFavorite
    }
  }
}
</script>

<style scoped>
.preference-page {
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

.favorites-section {
  margin-bottom: 40px;
}

.favorites-count {
  margin-bottom: 20px;
  text-align: right;
}

.favorites-count p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.food-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 24px;
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
  justify-content: flex-end;
}

.action-btn {
  padding: 10px 16px;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
}

.remove-btn {
  background: #ff6b6b;
  color: white;
}

.remove-btn:hover:not(:disabled) {
  background: #ff5252;
}

.remove-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* 載入中動畫 */
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

/* 無收藏訊息 */
.no-results {
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

.no-results p {
  margin: 0 0 8px;
  color: #666;
  font-size: 18px;
}

.no-results-subtitle {
  color: #999 !important;
  font-size: 14px !important;
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
  max-width: 400px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.modal-header {
  padding: 20px 24px 0;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  font-weight: 700;
  color: #333;
}

.modal-body {
  padding: 16px 24px;
}

.modal-body p {
  margin: 0;
  color: #666;
  line-height: 1.5;
}

.modal-actions {
  display: flex;
  gap: 12px;
  padding: 0 24px 24px;
}

.modal-btn {
  flex: 1;
  padding: 12px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 16px;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
}

.cancel-btn {
  background: #f5f5f5;
  color: #666;
}

.cancel-btn:hover {
  background: #e0e0e0;
}

.confirm-btn {
  background: #ff6b6b;
  color: white;
}

.confirm-btn:hover:not(:disabled) {
  background: #ff5252;
}

.confirm-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
}

/* 響應式設計 */
@media (max-width: 768px) {
  .food-grid {
    grid-template-columns: 1fr;
  }
  
  .food-details {
    grid-template-columns: 1fr;
  }
}</style>