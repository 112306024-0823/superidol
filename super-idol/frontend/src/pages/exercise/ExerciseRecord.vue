<template>
  <div class="exercise-record-page">
    <div class="container">
      <h1 class="page-title">運動記錄</h1>

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

      <div class="filter-row">
        <div class="filter-item">
          <label>日期 </label>
          <input type="date" v-model="selectedDate">
        </div>
        <div class="filter-item">
          <label>運動類型 </label>
          <select>
            <option>跑步</option>
            <option>游泳</option>
            <option>籃球</option>
            <option>羽球</option>
          </select>
        </div>
      </div>

      <!-- 卡路里燃燒摘要 -->
      <div class="calorie-summary">
        <div class="summary-item">
          <span class="summary-value">{{ dailySummary.totalCaloriesBurned }}</span>
          <span class="summary-label">卡路里燃燒</span>
        </div>
        <div class="summary-item">
          <span class="summary-value">{{ dailySummary.totalDuration }}</span>
          <span class="summary-label">運動時間 (分鐘)</span>
        </div>
        <div class="summary-item">
          <span class="summary-value">{{ dailySummary.exerciseCount }}</span>
          <span class="summary-label">運動次數</span>
        </div>
      </div>

      <!-- 運動記錄列表 -->
      <div class="exercise-list-container">
        <div class="list-header">
          <h2 class="section-title">今日運動</h2>
          <button class="btn btn-primary" @click="showAddExerciseModal = true">
            添加運動
          </button>
        </div>

        <div v-if="exercises.length" class="exercise-list">
          <!-- TODO: 使用 v-for 遍歷運動記錄 -->
          <div class="exercise-item">
            <div class="exercise-details">
              <div class="exercise-name">跑步</div>
              <div class="exercise-metrics">
                <span class="exercise-duration">30 分鐘</span>
                <span class="exercise-intensity">中等強度</span>
              </div>
            </div>
            <div class="exercise-calories">
              <span class="calories-value">-300</span>
              <span class="calories-label">卡路里</span>
            </div>
            <div class="exercise-actions">
              <button class="btn btn-icon btn-edit" @click="editExercise(1)">
                <i class="icon-edit"></i>
              </button>
              <button class="btn btn-icon btn-delete" @click="deleteExercise(1)">
                <i class="icon-delete"></i>
              </button>
            </div>
          </div>
        </div>

        <!-- 空狀態顯示 -->
        <div v-if="!exercises.length && !isLoading" class="empty-state">
          <p>今天還沒有運動記錄</p>
          <button class="btn btn-primary" @click="showAddExerciseModal = true">
            添加運動
          </button>
        </div>

        <!-- 載入中狀態 -->
        <div v-if="isLoading" class="loading-state">
          <p>載入中...</p>
        </div>
      </div>
    </div>

    <!-- 添加運動彈窗 (後續實現) -->
    <!-- TODO: 實現添加運動彈窗 -->
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
// TODO: 導入相關 store 和工具函數

export default {
  name: 'ExerciseRecord',
  setup() {
    // 當前選中的日期
    const selectedDate = ref(new Date())

    // 運動記錄
    const exercises = ref([])
    const isLoading = ref(false)

    // 添加運動彈窗
    const showAddExerciseModal = ref(false)
    const currentExercise = ref(null)

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
      // TODO: 實際實現中應計算所有運動的總和
      return {
        totalCaloriesBurned: 550,
        totalDuration: 75,
        exerciseCount: 2
      }
    })

    // 更改日期
    const changeDate = (days) => {
      const newDate = new Date(selectedDate.value)
      newDate.setDate(newDate.getDate() + days)
      selectedDate.value = newDate

      // 加載所選日期的運動記錄
      loadExerciseRecords()
    }

    // 加載運動記錄
    const loadExerciseRecords = async () => {
      isLoading.value = true
      try {
        // TODO: 從API獲取所選日期的運動記錄
        console.log('加載日期', selectedDate.value, '的運動記錄')

        // 模擬數據
        await new Promise(resolve => setTimeout(resolve, 500))
        exercises.value = [
          // 示例運動記錄數據
        ]
      } catch (error) {
        console.error('獲取運動記錄失敗:', error)
      } finally {
        isLoading.value = false
      }
    }

    // 添加運動記錄
    const addExercise = async (exerciseData) => {
      // TODO: 實現添加運動記錄功能
      console.log('添加運動:', exerciseData)
      showAddExerciseModal.value = false
      await loadExerciseRecords()
    }

    // 編輯運動記錄
    const editExercise = (exerciseId) => {
      // TODO: 實現編輯運動記錄功能
      console.log('編輯運動:', exerciseId)
      const exercise = exercises.value.find(e => e.id === exerciseId)
      if (exercise) {
        currentExercise.value = { ...exercise }
        showAddExerciseModal.value = true
      }
    }

    // 刪除運動記錄
    const deleteExercise = async (exerciseId) => {
      // TODO: 實現刪除運動記錄功能
      console.log('刪除運動:', exerciseId)
      await loadExerciseRecords()
    }

    // 初始化
    onMounted(() => {
      loadExerciseRecords()
    })

    return {
      selectedDate,
      formattedDate,
      exercises,
      isLoading,
      dailySummary,
      showAddExerciseModal,
      currentExercise,
      changeDate,
      addExercise,
      editExercise,
      deleteExercise
    }
  }
}
</script>

<style scoped>
.exercise-record-page {
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

.filter-row {
  display: flex;
  gap: 20px;
  margin: 16px 0;
  justify-content: center;
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
  /* 可以調整間距 */
  font-size: 14px;
  color: var(--text-color);
}

.filter-item select {
  padding: 6px 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
  font-size: 14px;
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
  padding: 24px;
  margin-bottom: 24px;
  display: flex;
  justify-content: space-around;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.summary-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.summary-value {
  font-size: 28px;
  font-weight: bold;
  margin-bottom: 8px;
  color: var(--text-color);
}

.summary-label {
  font-size: 14px;
  color: #666;
}

.exercise-list-container {
  background-color: var(--card-bg);
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-title {
  margin: 0;
  font-size: 20px;
  color: var(--text-color);
}

.exercise-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.exercise-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  background-color: rgba(0, 0, 0, 0.02);
  border-radius: 8px;
}

.exercise-details {
  flex: 1;
}

.exercise-name {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 4px;
  color: var(--text-color);
}

.exercise-metrics {
  display: flex;
  gap: 12px;
  font-size: 14px;
  color: #666;
}

.exercise-calories {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0 16px;
}

.calories-value {
  font-size: 20px;
  font-weight: bold;
  color: var(--success-color);
}

.calories-label {
  font-size: 12px;
  color: #666;
}

.exercise-actions {
  display: flex;
  gap: 8px;
}

.btn-edit {
  color: var(--primary-color);
}

.btn-delete {
  color: var(--danger-color);
}

.empty-state,
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 0;
  text-align: center;
}

.empty-state p,
.loading-state p {
  margin-bottom: 16px;
  color: #666;
  font-size: 18px;
}

@media (max-width: 768px) {
  .calorie-summary {
    flex-direction: column;
    gap: 20px;
  }

  .exercise-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .exercise-calories {
    margin: 12px 0;
  }

  .exercise-actions {
    align-self: flex-end;
  }
}
</style>