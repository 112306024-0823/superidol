<template>
  <div class="exercise-record-page">
    <div class="container">
      <h1 class="page-title">運動記錄</h1>








  <!-- 日期切換 -->
  <div class="date-selector">
    <button class="btn btn-icon" @click="changeDate(-1)">
      <i class="icon-left-arrow"></i>
    </button>
    <h2 class="current-date">{{ formattedDate }}</h2>
    <button class="btn btn-icon" @click="changeDate(1)">
      <i class="icon-right-arrow"></i>
    </button>
  </div>




  <!-- 篩選列 -->
  <div class="filter-row">
    <div class="filter-item">
      <label>日期</label>
      <input type="date" v-model="dateInput" @change="onDateChange" />
    </div>
    <div class="filter-item">
      <label>運動類型</label>
      <select v-model="filterType">
        <option value="">全部</option>
        <option v-for="type in exerciseTypes" :key="type">{{ type }}</option>
      </select>
    </div>
  </div>




  <!-- 每日摘要 -->
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
      <button class="btn btn-primary" @click="showAddExerciseModal = true">添加運動</button>
    </div>




    <div v-if="filteredExercises.length" class="exercise-list">
      <div v-for="exercise in filteredExercises" :key="exercise.id" class="exercise-item">
        <div class="exercise-details">
          <div class="exercise-name">{{ exercise.type }}</div>
          <div class="exercise-metrics">
            <span class="exercise-duration">{{ exercise.duration }} 分鐘</span>
          </div>
        </div>
        <div class="exercise-calories">
          <span class="calories-value">-{{ calculateCalories(exercise) }}</span>
          <span class="calories-label">卡路里</span>
        </div>
        <div class="exercise-actions">
          <button class="btn btn-icon btn-edit" @click="editExercise(exercise.id)">
            <i class="icon-edit"></i>
          </button>
          <button class="btn btn-icon btn-delete" @click="deleteExercise(exercise.id)">
            <i class="icon-delete"></i>
          </button>
        </div>
      </div>
    </div>




    <!-- 無資料/載入中 -->
    <div v-if="!filteredExercises.length && !isLoading" class="empty-state">
      <p>今天還沒有運動記錄</p>
    </div>
    <div v-if="isLoading" class="loading-state">
      <p>載入中...</p>
    </div>
  </div>
</div>




<!-- 添加運動彈窗 -->
<div v-if="showAddExerciseModal" class="modal-overlay" @click.self="closeModal">
  <div class="modal-content">
    <button class="close-button" @click="closeModal">×</button>




    <div class="modal-row">
      <label>運動類型</label>
      <select v-model="newExercise.type">
        <option v-for="type in exerciseTypes" :key="type">{{ type }}</option>
      </select>
    </div>




    <div class="modal-row">
      <label>運動時間 (分鐘)</label>
      <input type="number" min="0" step="1" v-model="newExercise.duration" />
    </div>




    <div class="modal-row">
      <button class="btn btn-primary" @click="submitExercise">確定</button>
    </div>
  </div>
</div>








  </div>
</template>




<script>
import { ref, computed, onMounted } from 'vue'




export default {
  name: 'ExerciseRecord',
  setup() {
    const selectedDate = ref(new Date())
    const dateInput = ref(selectedDate.value.toISOString().substr(0, 10))
    const exercises = ref([])
    const isLoading = ref(false)
    const showAddExerciseModal = ref(false)
    const newExercise = ref({ type: '', duration: '' })
    const filterType = ref('')




    const userId = '123'; // 實際應從登入狀態取得




    const exerciseTypes = [
      '籃球', '快走', '騎腳踏車', '健走', '伏地挺身',
      '攀岩', '划船', '跑步(8km/hr)', '跑步(10km/hr)',
      '足球', '游泳', '打太極', '慢走', '瑜珈'
    ]




    const formattedDate = computed(() => {
      return selectedDate.value.toLocaleDateString('zh-TW', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
      })
    })




    const fetchExerciseRecords = async () => {
      try {
        isLoading.value = true;
        const dateStr = selectedDate.value.toISOString().split("T")[0];
        const response = await fetch(`/api/exercise?date=${dateStr}&userId=${userId}`);
        const data = await response.json();
        records.value = data.map(record => ({
          ...record,
          calories: record.CaloriesBurned,
          duration: record.Duration,
          name: record.Exercise_Name,
          recordId: record.RecordID,
        }));
        updateSummary();
      } catch (error) {
        console.error("Error fetching records:", error);
        records.value = [];
        updateSummary();
      } finally {
        isLoading.value = false;
      }
    };
    const saveExercise = async () => {
      if (!newExercise.value.name || !newExercise.value.duration) return;




      const calories = calculateCalories(newExercise.value.name, newExercise.value.duration);
      const record = {
        UserID: userId,
        Date: selectedDate.value.toISOString().split("T")[0],
        Exercise_Name: newExercise.value.name,
        Duration: newExercise.value.duration,
        CaloriesBurned: calories,
      };




      try {
        const response = await fetch("/api/exercise", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(record),
        });




        if (!response.ok) throw new Error("新增失敗");




        const newRecord = await response.json();
        records.value.push({
          ...newRecord,
          calories,
          duration: newExercise.value.duration,
          name: newExercise.value.name,
          recordId: newRecord.RecordID,
        });




        updateSummary();
        showModal.value = false;
        newExercise.value = { name: "", duration: null };
      } catch (error) {
        console.error("Error saving record:", error);
      }
    };








    const METS = {
      籃球: 7.0,
      快走: 4.0,
      騎腳踏車: 6.0,
      健走: 6.0,
      伏地挺身: 5.0,
      攀岩: 8.0,
      划船: 7.0,
      '跑步(8km/hr)': 8.0,
      '跑步(10km/hr)': 10.0,
      足球: 7.0,
      游泳: 7.0,
      打太極: 4.0,
      慢走: 3.0,
      瑜珈: 5.0
    }




    const weight = 60 // 假設體重 60kg，這也可以改為動態資料




    const calculateCalories = (exercise) => {
      const MET = METS[exercise.type] || 1 // 若未找到對應 MET，預設為 1
      return Math.round(MET * weight * (exercise.duration / 60))
    }








    const filteredExercises = computed(() => {
      return filterType.value
        ? exercises.value.filter(e => e.type === filterType.value)
        : exercises.value
    })




    const dailySummary = computed(() => {
      const totalDuration = filteredExercises.value.reduce((sum, e) => sum + Number(e.duration), 0)
      const totalCaloriesBurned = filteredExercises.value.reduce((sum, e) => sum + calculateCalories(e), 0)
      return {
        totalDuration,
        totalCaloriesBurned,
        exerciseCount: filteredExercises.value.length
      }
    })




    const loadExerciseRecords = async () => {
      isLoading.value = true
      await new Promise(resolve => setTimeout(resolve, 300))
      exercises.value = [
        { id: 1, type: '跑步(8km/hr)', duration: 30 },
        { id: 2, type: '游泳', duration: 45 }
      ]
      isLoading.value = false
    }




    const submitExercise = async () => {
      if (!newExercise.value.type || !newExercise.value.duration) {
        alert('請填寫完整的運動資訊')
        return
      }




      const newId = Date.now()
      const minutes = Number(newExercise.value.duration)




      exercises.value.push({
        id: newId,
        type: newExercise.value.type,
        duration: Math.round(minutes)
      })




      closeModal()
    }




    const closeModal = () => {
      showAddExerciseModal.value = false
      newExercise.value = { type: '', duration: '' }
    }




    const changeDate = (days) => {
      const newDate = new Date(selectedDate.value)
      newDate.setDate(newDate.getDate() + days)
      selectedDate.value = newDate
      dateInput.value = newDate.toISOString().substr(0, 10)
      loadExerciseRecords()
    }




    const onDateChange = () => {
      selectedDate.value = new Date(dateInput.value)
      loadExerciseRecords()
    }




    const editExercise = (id) => {
      alert(`尚未實作編輯功能 (id: ${id})`)
    }




    const deleteExercise = (id) => {
      exercises.value = exercises.value.filter(e => e.id !== id)
    }




    onMounted(() => {
      loadExerciseRecords()
    })




    return {
      selectedDate,
      dateInput,
      formattedDate,
      exerciseTypes,
      filterType,
      exercises,
      filteredExercises,
      isLoading,
      dailySummary,
      showAddExerciseModal,
      newExercise,
      calculateCalories,
      closeModal,
      submitExercise,
      changeDate,
      onDateChange,
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
  color: orange;
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




.list-header button {
  background-color: orange;
  /* 鵝黃色 */
  color: white;
  border: none;
  border-radius: 10px;
  padding: 6px 15px;
  cursor: pointer;
  transition: background-color 0.3s;
}




.list-header button:hover {
  background-color: #f5d94b;
  /* 深一點的鵝黃色 */
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




.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}




.modal-content {
  background-color: white;
  border-radius: 8px;
  padding: 24px;
  position: relative;
  width: 90%;
  max-width: 200px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}




.close-button {
  position: absolute;
  top: 8px;
  right: 12px;
  background: none;
  border: none;
  font-size: 24px;
  color: red;
  cursor: pointer;
}




.modal-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
}




.modal-row button {
  background-color: #ffeb85;
  /* 鵝黃色 */
  color: #333;
  border: none;
  border-radius: 10px;
  padding: 6px 15px;
  cursor: pointer;
  transition: background-color 0.3s;
}




.modal-row button:hover {
  background-color: #f5d94b;
  /* 深一點的鵝黃色 */
}
</style>  




