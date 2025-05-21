<template>
  <div class="exercise-record-page">
    <div class="container">
      <h1 class="page-title">運動記錄</h1>

      <!-- 日期切換 - 優化設計 -->
      <div class="date-selector">
        <button class="btn btn-icon date-nav-btn" @click="changeDate(-1)">
          <span class="material-icons">chevron_left</span>
        </button>
        <div class="current-date-container">
          <h2 class="current-date">{{ formattedDate }}</h2>
          <input type="date" v-model="dateInput" @change="onDateChange" class="date-input" :max="today" />
        </div>
        <button class="btn btn-icon date-nav-btn" @click="changeDate(1)" :disabled="isToday">
          <span class="material-icons" :class="{ 'disabled-icon': isToday }">chevron_right</span>
        </button>
      </div>

      <!-- 篩選模式切換 -->
      <div class="filter-toggle">
        <span>篩選模式：</span>
        <div class="filter-mode-buttons">
          <button 
            class="btn-filter-mode" 
            :class="{ active: filterMode === 'day' }" 
            @click="switchFilterMode('day')">
            單日
          </button>
          <button 
            class="btn-filter-mode" 
            :class="{ active: filterMode === 'advanced' }" 
            @click="switchFilterMode('advanced')">
            進階篩選
          </button>
        </div>
      </div>

      <!-- 進階篩選面板 - 僅在進階模式顯示 -->
      <div v-if="filterMode === 'advanced'" class="filter-row">
        <!-- 月份選擇器 -->
        <div class="filter-item filter-month">
          <label>月份選擇</label>
          <div class="month-selector">
            <button 
              class="btn btn-month" 
              @click="selectMonth(new Date())" 
              :class="{ active: isCurrentMonthSelected }">
              本月
            </button>
            <select v-model="selectedMonth" class="month-dropdown" @change="applyMonthFilter">
              <option value="">選擇其他月份</option>
              <option v-for="(month, index) in availableMonths" :key="index" :value="month.value">
                {{ month.label }}
              </option>
            </select>
          </div>
        </div>

        <div class="filter-item filter-date-range">
          <label>日期區間</label>
          <div class="date-range-inputs">
            <div class="date-input-group">
              <span class="date-label">從</span>
              <input type="date" v-model="startDateFilter" @change="applyDateRangeFilter" :max="today" class="date-range-input" />
            </div>
            <div class="date-input-group">
              <span class="date-label">至</span>
              <input type="date" v-model="endDateFilter" @change="applyDateRangeFilter" :max="today" class="date-range-input" />
            </div>
          </div>
        </div>
      </div>
      
      <!-- 篩選標籤 - 新增 -->
      <div class="filter-info" v-if="filterMode === 'advanced' && isDateRangeActive">
        <div class="tag-container">
          <div v-if="isDateRangeActive" class="filter-tag">
            <span>{{ formatDateRangeText }}</span>
            <button class="clear-tag" @click="clearDateRangeFilter">×</button>
          </div>
        </div>
        <button v-if="isDateRangeActive" class="clear-all-filters" @click="clearAllFilters">
          清除所有篩選
        </button>
      </div>

      <!-- 每日摘要 - 優化視覺效果 -->
      <div class="calorie-summary">
        <div class="summary-item">
          <div class="summary-icon">
            <span class="material-icons">local_fire_department</span>
          </div>
          <span class="summary-value">{{ dailySummary.totalCaloriesBurned }}</span>
          <span class="summary-label">卡路里燃燒</span>
        </div>
        <div class="summary-item">
          <div class="summary-icon">
            <span class="material-icons">timer</span>
          </div>
          <span class="summary-value">{{ dailySummary.totalDuration }}</span>
          <span class="summary-label">運動時間 (分鐘)</span>
        </div>
        <div class="summary-item">
          <div class="summary-icon">
            <span class="material-icons">fitness_center</span>
          </div>
          <span class="summary-value">{{ dailySummary.exerciseCount }}</span>
          <span class="summary-label">運動次數</span>
        </div>
      </div>

      <!-- 運動記錄列表 -->
      <div class="exercise-list-container">
        <div class="list-header">
          <h2 class="section-title">運動列表</h2>
          <button class="btn btn-primary add-btn" @click="openAddExerciseModal">
            <span class="material-icons">add</span>新增運動記錄
          </button>
        </div>

        <!-- 圖表顯示區 - 新增 -->
        <div v-if="filteredExercises.length" class="exercise-chart">
          <div class="chart-header">
            <span>今日運動分佈</span>
          </div>
          <div class="chart-content">
            <div v-for="exercise in filteredExercises" :key="exercise.id" 
                class="chart-bar" 
                :style="{width: `${(exercise.duration / dailySummary.totalDuration) * 100}%`}">
              <div class="bar-label">{{ exercise.type }}</div>
            </div>
          </div>
        </div>

        <div v-if="filteredExercises.length" class="exercise-list">
          <div v-for="exercise in filteredExercises" :key="exercise.id" class="exercise-item">
            <!-- 日期顯示 - 條件渲染，僅在日期範圍篩選時顯示 -->
            <div v-if="isDateRangeActive" class="exercise-date">
              {{ formatShortDate(exercise.date) }}
            </div>
            
            <!-- 運動圖示 - 新增 -->
            <div class="exercise-icon">
              <span class="material-icons">{{ getExerciseIcon(exercise.type) }}</span>
            </div>
            
            <div class="exercise-details">
              <div class="exercise-name">{{ exercise.type }}</div>
              <div class="exercise-metrics">
                <span class="exercise-duration">
                  <span class="material-icons small-icon">timer</span>
                  {{ exercise.duration }} 分鐘
                </span>
                <span class="exercise-intensity">
                  <span class="material-icons small-icon">speed</span>
                  <span class="intensity-level">{{ getIntensityLevel(exercise.type) }}</span>
                  <span class="flame-icons">
                    <span class="material-icons flame-icon" v-for="n in getFlameCount(exercise.type)" :key="n">local_fire_department</span>
                  </span>
                </span>
              </div>
            </div>
            <div class="exercise-calories">
              <span class="calories-value">-{{ calculateCalories(exercise) }}</span>
              <span class="calories-label">卡路里</span>
            </div>
            <div class="exercise-actions">
              <button class="btn btn-icon btn-edit" @click="editExercise(exercise.id)" :disabled="isDeleting === exercise.id">
                <span class="material-icons">edit</span>
              </button>
              <button class="btn btn-icon btn-delete" @click="deleteExercise(exercise.id)" :disabled="isDeleting === exercise.id">
                <span class="material-icons">{{ isDeleting === exercise.id ? 'hourglass_empty' : 'delete' }}</span>
              </button>
            </div>
          </div>
        </div>

        <!-- 無資料/載入中 -->
        <div v-if="!filteredExercises.length && !isLoading" class="empty-state">
          <span class="material-icons empty-icon">fitness_center</span>
          <p>今天還沒有運動記錄</p>
          <button class="btn btn-primary" @click="openAddExerciseModal">
            開始記錄運動
          </button>
        </div>
        <div v-if="isLoading" class="loading-state">
          <div class="spinner"></div>
          <p>載入中...</p>
        </div>
      </div>
    </div>

    <!-- 添加運動彈窗 - 優化設計 -->
    <div v-if="showAddExerciseModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>新增運動記錄</h3>
          <button class="close-button" @click="closeModal">×</button>
        </div>

        <div class="modal-body">
          <div class="modal-row">
            <label>運動類型</label>
            <select v-model="newExercise.type" class="modal-input">
              <option value="" disabled>請選擇運動類型</option>
              <option v-for="type in exerciseTypes" :key="type" :value="type">
                {{ type }} ({{ getIntensityLevel(type) }} 
                <span v-html="getFlameIconsHTML(type)"></span>)
              </option>
            </select>
          </div>

          <div class="modal-row">
            <label>運動時間 (分鐘)</label>
            <input type="number" min="1" step="1" v-model="newExercise.duration" class="modal-input" />
          </div>
          
          <div class="modal-row">
            <label>日期</label>
            <input type="date" v-model="newExercise.date" class="modal-input" :max="today" />
          </div>

          <!-- 預估效果顯示 - 新增 -->
          <div v-if="newExercise.type && newExercise.duration" class="modal-preview">
            <div class="preview-item">
              <span class="preview-label">預估消耗</span>
              <span class="preview-value">{{ calculateNewExerciseCalories() }} 卡路里</span>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn btn-secondary" @click="closeModal" :disabled="isSubmitting">取消</button>
          <button class="btn btn-primary" @click="submitExercise" :disabled="!newExercise.type || !newExercise.duration || !newExercise.date || isSubmitting">
            {{ isSubmitting ? '處理中...' : '確定新增' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 編輯運動彈窗 - 新增 -->
    <div v-if="showEditExerciseModal" class="modal-overlay" @click.self="closeEditModal">
      <div class="modal-content">
        <div class="modal-header">
          <h3>編輯運動記錄</h3>
          <button class="close-button" @click="closeEditModal">×</button>
        </div>

        <div class="modal-body">
          <div class="modal-row">
            <label>運動類型</label>
            <select v-model="editingExercise.type" class="modal-input">
              <option value="" disabled>請選擇運動類型</option>
              <option v-for="type in exerciseTypes" :key="type" :value="type">
                {{ type }} ({{ getIntensityLevel(type) }} 
                <span v-html="getFlameIconsHTML(type)"></span>)
              </option>
            </select>
          </div>

          <div class="modal-row">
            <label>運動時間 (分鐘)</label>
            <input type="number" min="1" step="1" v-model="editingExercise.duration" class="modal-input" />
          </div>

          <div class="modal-row">
            <label>日期</label>
            <input type="date" v-model="editingExercise.date" class="modal-input" :max="today" />
          </div>

          <!-- 預估效果顯示 -->
          <div v-if="editingExercise.type && editingExercise.duration" class="modal-preview">
            <div class="preview-item">
              <span class="preview-label">預估消耗</span>
              <span class="preview-value">{{ calculateEditingExerciseCalories() }} 卡路里</span>
            </div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn btn-secondary" @click="closeEditModal" :disabled="isEditing">取消</button>
          <button 
            class="btn btn-primary" 
            @click="submitEditExercise" 
            :disabled="!editingExercise.type || !editingExercise.duration || !editingExercise.date || isEditing">
            {{ isEditing ? '處理中...' : '確定修改' }}
          </button>
        </div>
      </div>
    </div>

    <!-- 通知彈窗 -->
    <div v-if="notification.show" class="notification-overlay">
      <div class="notification-content" :class="notification.type">
        <span class="material-icons notification-icon" v-if="notification.type === 'success'">check_circle</span>
        <span class="material-icons notification-icon" v-else>error</span>
        <p>{{ notification.message }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { api } from '@/services/api'
import { useAuthStore } from '@/store/auth'
import axios from 'axios'

export default {
  name: 'ExerciseRecord',
  setup() {
    const selectedDate = ref(new Date())
    const dateInput = ref(selectedDate.value.toISOString().substr(0, 10))
    const exercises = ref([])
    const isLoading = ref(false)
    const showAddExerciseModal = ref(false)
    const newExercise = ref({ type: '', duration: '', date: '' })
    const filterType = ref('')
    const authStore = useAuthStore()
    const exerciseTypes = ref([]) // 從API獲取的運動類型名稱
    const exerciseItems = ref([]) // 包含完整運動項目資料（含MET值）
    const isLoadingExerciseTypes = ref(false)
    const today = ref(new Date().toISOString().split('T')[0])
    const startDateFilter = ref('')
    const endDateFilter = ref('')
    const showEditExerciseModal = ref(false)
    const editingExercise = ref({ type: '', duration: '', date: '' })
    
    // 添加操作狀態
    const isSubmitting = ref(false)
    const isDeleting = ref(null)
    const isEditing = ref(false)
    
    // 添加通知訊息
    const notification = ref({ show: false, message: '', type: 'success' })
    
    // 顯示通知
    const showNotification = (message, type = 'success') => {
      notification.value = { show: true, message, type }
      const displayTime = type === 'error' ? 5000 : 3000; // 錯誤訊息顯示更久
      setTimeout(() => {
        notification.value.show = false
      }, displayTime)
    }
    
    // 計算屬性: 檢查當前選擇日期是否為今天 - 新增
    const isToday = computed(() => {
      const currentDate = selectedDate.value.toISOString().split('T')[0]
      return currentDate >= today.value
    })
    
    // 計算屬性: 日期範圍篩選是否激活 - 新增
    const isDateRangeActive = computed(() => {
      return startDateFilter.value || endDateFilter.value
    })
    
    // 計算屬性: 格式化日期範圍文字 - 新增
    const formatDateRangeText = computed(() => {
      if (startDateFilter.value && endDateFilter.value) {
        return `${formatLocalDate(startDateFilter.value)} - ${formatLocalDate(endDateFilter.value)}`
      } else if (startDateFilter.value) {
        return `${formatLocalDate(startDateFilter.value)} 之後`
      } else if (endDateFilter.value) {
        return `${formatLocalDate(endDateFilter.value)} 之前`
      }
      return ''
    })
    
    // 格式化日期為本地格式 (例如: 2023年1月1日) - 新增
    const formatLocalDate = (dateString) => {
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-TW', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
    
    // 格式化日期為簡短格式 (例如: 01/21) - 新增
    const formatShortDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-TW', {
        month: '2-digit',
        day: '2-digit'
      })
    }
    
    // 應用日期範圍篩選 - 新增
    const applyDateRangeFilter = () => {
      // 切換到進階篩選模式
      filterMode.value = 'advanced'
      loadExerciseRecords()
    }
    
    // 清除日期範圍篩選 - 新增
    const clearDateRangeFilter = (skipReload = false) => {
      startDateFilter.value = ''
      endDateFilter.value = ''
      if (!skipReload) {
        loadExerciseRecords()
      }
    }
    
    // 清除所有篩選條件 - 新增
    const clearAllFilters = () => {
      clearDateRangeFilter()
    }

    // 從 authStore 獲取使用者資料
    const userId = computed(() => authStore.user?.id || null)
    const weight = computed(() => authStore.user?.weight || 60)

    // 從後端獲取運動項目列表
    const loadExerciseItems = async () => {
      isLoadingExerciseTypes.value = true
      try {
        const { data } = await api.get('/api/exercise/items')
        if (data && data.items && data.items.length > 0) {
          // 保存完整運動項目資料，包含MET值
          exerciseItems.value = data.items
          // 提取運動名稱用於下拉選單
          exerciseTypes.value = data.items.map(item => item.Exercise_Name)
          console.log(`成功載入 ${data.items.length} 項運動類型`)
        } else {
          exerciseItems.value = []
          exerciseTypes.value = []
          console.warn('API返回了空的運動項目列表，可能是資料庫中沒有ExerciseItem表或表中沒有數據')
        }
      } catch (error) {
        console.error('載入運動項目失敗:', error)
        exerciseItems.value = []
        exerciseTypes.value = []
      } finally {
        isLoadingExerciseTypes.value = false
      }
    }

    const formattedDate = computed(() => {
      return selectedDate.value.toLocaleDateString('zh-TW', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long'
      })
    })

    const loadExerciseRecords = async () => {
      isLoading.value = true;
      let retryCount = 0;
      const maxRetries = 2;
      
      const loadData = async () => {
        try {
          // 建立API請求參數
          const params = {
            user_id: userId.value
          }
          
          // 根據篩選模式設置查詢參數
          if (filterMode.value === 'day') {
            // 單日模式 - 使用頂部日期選擇器
            const dateStr = selectedDate.value.toISOString().split('T')[0]
            params.start_date = dateStr
            params.end_date = dateStr
          } else if (filterMode.value === 'advanced') {
            // 進階篩選模式 - 使用日期範圍或月份
            if (isDateRangeActive.value) {
              if (startDateFilter.value) params.start_date = startDateFilter.value
              if (endDateFilter.value) params.end_date = endDateFilter.value
            }
          }
          
          // 增加超時設定
          const { data } = await api.get('/api/exercise/records', { 
            params,
            timeout: 30000 // 增加到30秒
          });
          
          exercises.value = (data.records || []).map(r => ({
            id: r.RecordID || r.record_id,
            type: r.Exercise_Name || r.exercise_name,
            duration: r.Duration || r.duration,
            calories_burned: r.calories_burned,
            date: r.Date || r.date // 添加日期屬性，用於多日期篩選顯示
          }));
          
          return true; // 請求成功
        } catch (error) {
          console.error('載入運動紀錄失敗:', error);
          
          // 檢查是否為超時錯誤
          if (error.code === 'ECONNABORTED' && retryCount < maxRetries) {
            retryCount++;
            console.log(`請求超時，進行第 ${retryCount} 次重試...`);
            return false; // 請求失敗，需要重試
          }
          
          // 其他錯誤或超過重試次數
          let errorMessage = '載入資料時發生錯誤';
          
          if (error.code === 'ECONNABORTED') {
            errorMessage = '伺服器回應時間過長，請稍後再試';
          } else if (error.response) {
            errorMessage = `錯誤 (${error.response.status}): ${error.response.data.message || '未知錯誤'}`;
          }
          
          // 顯示錯誤通知
          showNotification(errorMessage, 'error');
          exercises.value = [];
          return true; // 不再重試
        }
      };
      
      // 嘗試載入數據，如果失敗則重試
      let success = false;
      while (!success && retryCount <= maxRetries) {
        success = await loadData();
        
        // 如果失敗且需要重試，等待一段時間
        if (!success) {
          await new Promise(resolve => setTimeout(resolve, 2000)); // 等待2秒再重試
        }
      }
      
      isLoading.value = false;
    }

    const submitExercise = async () => {
      if (!newExercise.value.type || !newExercise.value.duration || !newExercise.value.date) {
        alert('請填寫完整的運動資訊')
        return
      }
      
      isSubmitting.value = true
      
      try {
        await api.post('/api/exercise/log', {
          user_id: userId.value,
          exercise_name: newExercise.value.type,
          duration: Number(newExercise.value.duration),
          date: newExercise.value.date
        })
        await loadExerciseRecords()
        closeModal()
        showNotification('運動紀錄已成功新增')
      } catch (error) {
        showNotification('新增運動紀錄失敗: ' + (error.response?.data?.error || error.message), 'error')
        console.error(error)
      } finally {
        isSubmitting.value = false
      }
    }

    const deleteExercise = async (id) => {
      if (!confirm('確定要刪除這筆運動紀錄嗎？')) return
      
      isDeleting.value = id
      
      try {
        await api.delete(`/api/exercise/${id}`, { params: { user_id: userId.value } })
        await loadExerciseRecords()
        showNotification('運動記錄已成功刪除')
      } catch (error) {
        showNotification('刪除失敗: ' + (error.response?.data?.error || error.message), 'error')
        console.error(error)
      } finally {
        isDeleting.value = null
      }
    }

    const closeModal = () => {
      showAddExerciseModal.value = false
      newExercise.value = { type: '', duration: '', date: '' }
    }

    const onDateChange = () => {
      selectedDate.value = new Date(dateInput.value)
      // 當手動選擇日期時，自動切換到單日模式
      switchFilterMode('day')
      loadExerciseRecords()
    }

    const changeDate = (days) => {
      const newDate = new Date(selectedDate.value)
      newDate.setDate(newDate.getDate() + days)
      selectedDate.value = newDate
      dateInput.value = newDate.toISOString().substr(0, 10)
      // 使用箭頭切換日期時，自動切換到單日模式
      switchFilterMode('day')
    }

    const editExercise = (id) => {
      const exercise = exercises.value.find(e => e.id === id)
      if (exercise) {
        editingExercise.value = {
          id: exercise.id,
          type: exercise.type,
          duration: exercise.duration,
          date: exercise.date || selectedDate.value.toISOString().split('T')[0]
        }
        showEditExerciseModal.value = true
      }
    }

    // 從後端資料獲取MET值
    const getMET = (exerciseName) => {
      // 從已載入的運動項目資料中尋找匹配的MET值
      const item = exerciseItems.value.find(item => item.Exercise_Name === exerciseName)
      return item && item.MET ? parseFloat(item.MET) : 0
    }

    // 根據 MET 值取得運動強度等級
    const getIntensityLevel = (exerciseName) => {
      const met = getMET(exerciseName)
      if (met <= 0) return '未知強度'
      if (met < 3) return '輕度'
      if (met < 6) return '中度'
      return '高度'
    }
    
    // 根據 MET 值獲取火焰數量 (1-5)
    const getFlameCount = (exerciseName) => {
      const met = getMET(exerciseName)
      if (met <= 0) return 0
      if (met < 2) return 1
      if (met < 4) return 2
      if (met < 6) return 3
      if (met < 8) return 4
      return 5
    }
    
    // 獲取用於 HTML 選項的火焰圖示字串
    const getFlameIconsHTML = (exerciseName) => {
      const count = getFlameCount(exerciseName)
      return '🔥'.repeat(count)
    }

    // 為運動類型提供對應圖示 - 新增
    const getExerciseIcon = (exerciseType) => {
      const iconMap = {
        '籃球': 'sports_basketball',
        '快走': 'directions_walk',
        '騎腳踏車': 'pedal_bike',
        '健走': 'hiking',
        '伏地挺身': 'fitness_center',
        '攀岩': 'terrain',
        '划船': 'rowing',
        '跑步(8km/hr)': 'directions_run',
        '跑步(10km/hr)': 'directions_run',
        '足球': 'sports_soccer',
        '游泳': 'pool',
        '打太極': 'self_improvement',
        '慢走': 'directions_walk',
        '瑜珈': 'self_improvement'
      }
      return iconMap[exerciseType] || 'fitness_center'
    }

    const calculateCalories = (exercise) => {
      // 如果後端已經計算好卡路里，直接使用
      if (exercise.calories_burned !== undefined) {
        return Math.round(exercise.calories_burned)
      }
      
      // 否則使用前端計算（與後端公式保持一致）
      const MET = getMET(exercise.type)
      return Math.round(MET * 3.5 * weight.value / 200 * exercise.duration)
    }

    // 計算新運動記錄的預估卡路里 - 新增
    const calculateNewExerciseCalories = () => {
      if (!newExercise.value.type || !newExercise.value.duration) return 0
      const MET = getMET(newExercise.value.type)
      return Math.round(MET * 3.5 * weight.value / 200 * newExercise.value.duration)
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

    const submitEditExercise = async () => {
      if (!editingExercise.value.type || !editingExercise.value.duration || !editingExercise.value.date) {
        alert('請填寫完整的運動資訊')
        return
      }
      
      isEditing.value = true
      
      try {
        const response = await api.put(`/api/exercise/${editingExercise.value.id}`, {
          user_id: userId.value,
          exercise_name: editingExercise.value.type,
          duration: Number(editingExercise.value.duration),
          date: editingExercise.value.date
        })
        
        if (response.data.message) {
          showNotification('運動記錄已成功更新')
        }
        
        await loadExerciseRecords()
        closeEditModal()
      } catch (error) {
        showNotification('修改運動紀錄失敗: ' + (error.response?.data?.error || error.message), 'error')
        console.error(error)
      } finally {
        isEditing.value = false
      }
    }

    const calculateEditingExerciseCalories = () => {
      if (!editingExercise.value.type || !editingExercise.value.duration) return 0
      const MET = getMET(editingExercise.value.type)
      return Math.round(MET * 3.5 * weight.value / 200 * editingExercise.value.duration)
    }

    const closeEditModal = () => {
      showEditExerciseModal.value = false
      editingExercise.value = { type: '', duration: '', date: '' }
    }

    // 添加月份篩選 - 新增
    const selectedMonth = ref('')
    const isCurrentMonthSelected = ref(false)
    
    // 計算可選月份列表 (只顯示2025年1月到5月)
    const availableMonths = computed(() => {
      const months = [];
      
      // 只添加2025年1月到5月
      for (let month = 0; month < 5; month++) {
        const date = new Date(2025, month, 1);
        months.push({
          label: date.toLocaleDateString('zh-TW', { year: 'numeric', month: 'long' }),
          value: date.toISOString().split('T')[0].substring(0, 7) // YYYY-MM 格式
        });
      }
      
      return months;
    })
    
    // 月份選擇處理
    const selectMonth = (date) => {
      const year = date.getFullYear()
      const month = date.getMonth()
      
      // 月份開始和結束日期
      const firstDay = new Date(year, month, 1)
      const lastDay = new Date(year, month + 1, 0)
      
      // 格式化為 YYYY-MM-DD
      startDateFilter.value = firstDay.toISOString().split('T')[0]
      endDateFilter.value = lastDay.toISOString().split('T')[0]
      
      // 更新選中狀態
      const currentDate = new Date()
      isCurrentMonthSelected.value = currentDate.getMonth() === month && currentDate.getFullYear() === year
      
      // 清除下拉選擇
      selectedMonth.value = ''
      
      // 切換到進階篩選模式
      filterMode.value = 'advanced'
      
      // 應用篩選
      applyDateRangeFilter()
    }
    
    // 下拉選擇月份
    const applyMonthFilter = () => {
      if (!selectedMonth.value) return
      
      const [year, month] = selectedMonth.value.split('-')
      const date = new Date(parseInt(year), parseInt(month) - 1, 1)
      selectMonth(date)
      
      // 重置按鈕狀態
      isCurrentMonthSelected.value = false
    }

    // 打開新增運動彈窗
    const openAddExerciseModal = () => {
      // 初始化日期為當前選擇的日期
      newExercise.value = { 
        type: '', 
        duration: '', 
        date: selectedDate.value.toISOString().split('T')[0]
      }
      showAddExerciseModal.value = true
    }

    // 添加篩選模式切換
    const filterMode = ref('day')
    const switchFilterMode = (mode) => {
      filterMode.value = mode
      if (mode === 'day') {
        clearDateRangeFilter(true)
      }
      loadExerciseRecords()
    }

    // 初始化API服務時設定全局超時
    const initializeApiService = () => {
      // 預先設定API全局請求超時
      axios.defaults.timeout = 20000; // 設定全局20秒超時
      
      // 也可以在這裡設定全局的請求攔截器，用於統一處理錯誤
      axios.interceptors.response.use(
        response => response,
        error => {
          // 處理超時錯誤
          if (error.code === 'ECONNABORTED' && error.message && error.message.includes('timeout')) {
            console.error('API請求超時');
          }
          return Promise.reject(error);
        }
      );
    }

    // 在onMounted前添加
    initializeApiService();

    onMounted(async () => {
      // 若未登入或無用戶資料，先獲取用戶資料
      if (!authStore.user && authStore.isAuthenticated) {
        await authStore.fetchUserData()
      }
      
      // 加載運動項目
      await loadExerciseItems()
      
      // 設置初始日期為今天
      selectedDate.value = new Date()
      dateInput.value = selectedDate.value.toISOString().substr(0, 10)
      
      // 設置初始模式為單日模式
      filterMode.value = 'day'
      
      // 加載運動記錄（當前日期）
      loadExerciseRecords()
      
      // 添加Material Icons - 新增
      const link = document.createElement('link')
      link.rel = 'stylesheet'
      link.href = 'https://fonts.googleapis.com/icon?family=Material+Icons'
      document.head.appendChild(link)
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
      isLoadingExerciseTypes,
      dailySummary,
      showAddExerciseModal,
      newExercise,
      calculateCalories,
      calculateNewExerciseCalories,
      closeModal,
      submitExercise,
      changeDate,
      onDateChange,
      editExercise,
      deleteExercise,
      getMET,
      getIntensityLevel,
      getFlameCount,
      getFlameIconsHTML,
      getExerciseIcon,
      today,
      isToday,
      startDateFilter,
      endDateFilter,
      isDateRangeActive,
      formatDateRangeText,
      applyDateRangeFilter,
      clearDateRangeFilter,
      clearAllFilters,
      formatShortDate,
      showEditExerciseModal,
      editingExercise,
      submitEditExercise,
      calculateEditingExerciseCalories,
      closeEditModal,
      isSubmitting,
      isDeleting,
      isEditing,
      notification,
      showNotification,
      selectedMonth,
      isCurrentMonthSelected,
      availableMonths,
      selectMonth,
      applyMonthFilter,
      openAddExerciseModal,
      filterMode,
      switchFilterMode
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
  text-align: center;
}

/* 日期選擇器優化 */
.date-selector {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
  position: relative;
}

.date-nav-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  transition: background-color 0.3s;
}

.date-nav-btn:hover {
  background-color: rgba(0,0,0,0.05);
}

.current-date-container {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.current-date {
  margin: 0 16px;
  font-size: 20px;
  color: var(--text-color);
  cursor: pointer;
}

.date-input {
  position: absolute;
  opacity: 0;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.filter-row {
  display: flex;
  gap: 20px;
  margin: 16px 0;
  justify-content: center;
  flex-wrap: wrap;
  background-color: var(--card-bg);
  border-radius: 12px;
  padding: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  color: var(--text-color);
}

.filter-select {
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-size: 14px;
  min-width: 150px;
  background-color: white;
}

.filter-date-range {
  flex-direction: column;
  align-items: flex-start;
}

.date-range-inputs {
  display: flex;
  gap: 10px;
  align-items: center;
}

.date-input-group {
  display: flex;
  align-items: center;
  gap: 5px;
}

.date-label {
  font-size: 12px;
  color: #666;
}

.date-range-input {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 14px;
}

.filter-tags {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 10px 0 20px;
}

.tag-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-tag {
  display: flex;
  align-items: center;
  background-color: rgba(255, 165, 0, 0.1);
  border-radius: 50px;
  padding: 5px 12px;
  font-size: 14px;
  color: #555;
}

.clear-tag {
  background: none;
  border: none;
  font-size: 16px;
  color: #999;
  margin-left: 8px;
  cursor: pointer;
}

.clear-all-filters {
  background: none;
  border: none;
  color: #f44336;
  font-size: 14px;
  cursor: pointer;
  text-decoration: underline;
}

.disabled-icon {
  color: #ccc;
}

/* 摘要卡片優化 */
.calorie-summary {
  background-color: var(--card-bg);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  display: flex;
  justify-content: space-around;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.summary-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 0 10px;
}

.summary-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: rgba(255, 165, 0, 0.1);
  margin-bottom: 12px;
}

.summary-icon .material-icons {
  font-size: 28px;
  color: orange;
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

/* 運動列表容器優化 */
.exercise-list-container {
  background-color: var(--card-bg);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #eee;
}

.add-btn {
  background-color: orange;
  color: white;
  border: none;
  border-radius: 50px;
  padding: 8px 20px;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.add-btn:hover {
  background-color: #f5a623;
}

.section-title {
  margin: 0;
  font-size: 20px;
  color: var(--text-color);
}

/* 運動列表圖表 - 新增 */
.exercise-chart {
  margin-bottom: 24px;
  padding: 16px;
  background-color: rgba(0,0,0,0.02);
  border-radius: 8px;
}

.chart-header {
  margin-bottom: 12px;
  font-weight: 500;
  color: #555;
}

.chart-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.chart-bar {
  position: relative;
  height: 30px;
  background-color: orange;
  border-radius: 4px;
  min-width: 30px;
  display: flex;
  align-items: center;
  padding-left: 10px;
  transition: width 0.5s ease;
}

.bar-label {
  color: white;
  font-size: 12px;
  font-weight: 500;
  white-space: nowrap;
  text-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

/* 運動列表項目優化 */
.exercise-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.exercise-item {
  display: flex;
  align-items: center;
  padding: 16px;
  background-color: rgba(0, 0, 0, 0.02);
  border-radius: 12px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.exercise-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.exercise-date {
  font-size: 12px;
  color: #888;
  background-color: rgba(0,0,0,0.03);
  padding: 2px 8px;
  border-radius: 4px;
  margin-bottom: 8px;
  align-self: flex-start;
}

.exercise-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background-color: rgba(255, 165, 0, 0.1);
  border-radius: 8px;
  margin-right: 16px;
}

.exercise-icon .material-icons {
  color: orange;
}

.exercise-details {
  flex: 1;
}

.exercise-name {
  font-size: 18px;
  font-weight: 500;
  margin-bottom: 6px;
  color: var(--text-color);
}

.exercise-metrics {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: #666;
}

.exercise-intensity {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #666;
}

.intensity-level {
  font-weight: 500;
}

.flame-icons {
  display: inline-flex;
}

.flame-icon {
  font-size: 14px;
  color: #ff6b00;
}

.small-icon {
  font-size: 14px;
  vertical-align: middle;
  margin-right: 4px;
}

.exercise-calories {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0 16px;
  min-width: 70px;
}

.calories-value {
  font-size: 20px;
  font-weight: bold;
  color: #4caf50;
}

.calories-label {
  font-size: 12px;
  color: #666;
}

.exercise-actions {
  display: flex;
  gap: 8px;
}

.btn-edit, .btn-delete {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s;
}

.btn-edit {
  color: #2196f3;
}

.btn-delete {
  color: #f44336;
}

.btn-edit:hover, .btn-delete:hover {
  background-color: rgba(0,0,0,0.05);
}

/* 空狀態和載入中優化 */
.empty-state,
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  text-align: center;
}

.empty-icon {
  font-size: 48px;
  color: #ccc;
  margin-bottom: 16px;
}

.empty-state p,
.loading-state p {
  margin-bottom: 20px;
  color: #666;
  font-size: 18px;
}

.empty-state button {
  background-color: orange;
  color: white;
  border: none;
  border-radius: 50px;
  padding: 10px 24px;
  font-weight: 500;
}

/* 載入中動畫 */
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(255, 165, 0, 0.1);
  border-left-color: orange;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* 彈窗優化 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 12px;
  position: relative;
  width: 90%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

.modal-header {
  padding: 16px 24px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 20px;
  color: #333;
}

.close-button {
  background: none;
  border: none;
  font-size: 24px;
  color: #999;
  cursor: pointer;
  transition: color 0.3s;
}

.close-button:hover {
  color: #f44336;
}

.modal-body {
  padding: 24px;
}

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.modal-row {
  margin-bottom: 20px;
}

.modal-row label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.modal-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
}

.modal-preview {
  margin-top: 24px;
  padding: 16px;
  background-color: rgba(255, 165, 0, 0.05);
  border-radius: 8px;
}

.preview-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.preview-label {
  color: #666;
}

.preview-value {
  font-weight: 500;
  color: orange;
}

.btn-secondary {
  background-color: #f5f5f5;
  color: #333;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  cursor: pointer;
}

.btn-primary {
  background-color: orange;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 20px;
  cursor: pointer;
}

.btn-primary:disabled {
  background-color: #ffd699;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .calorie-summary {
    flex-direction: column;
    gap: 20px;
  }

  .exercise-item {
    flex-wrap: wrap;
  }

  .exercise-calories {
    margin: 12px 0;
    order: 3;
    width: 100%;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    gap: 8px;
  }

  .exercise-actions {
    order: 2;
  }
}

/* 通知彈窗 */
.notification-overlay {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1001;
  animation: slideIn 0.3s forwards;
}

@keyframes slideIn {
  from { transform: translateX(100%); opacity: 0; }
  to { transform: translateX(0); opacity: 1; }
}

.notification-content {
  background-color: white;
  border-radius: 8px;
  padding: 12px 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  border-left: 4px solid;
}

.notification-content.success {
  border-left-color: #4caf50;
}

.notification-content.success .notification-icon {
  color: #4caf50;
}

.notification-content.error {
  border-left-color: #f44336;
}

.notification-content.error .notification-icon {
  color: #f44336;
}

.notification-content p {
  margin: 0;
  font-size: 16px;
  color: #333;
}

.notification-icon {
  font-size: 24px;
  margin-right: 8px;
}

/* 月份選擇器樣式 */
.filter-month {
  margin-bottom: 16px;
}

.month-selector {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
  margin-top: 8px;
}

.btn-month {
  background-color: #f5f5f5;
  color: #333;
  border: none;
  border-radius: 20px;
  padding: 6px 16px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-month:hover {
  background-color: #e0e0e0;
}

.btn-month.active {
  background-color: orange;
  color: white;
  box-shadow: 0 2px 5px rgba(255, 165, 0, 0.3);
}

.month-dropdown {
  padding: 6px 12px;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-size: 14px;
  background-color: white;
}

/* 篩選模式切換樣式 */
.filter-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin: 24px 0;
}

.filter-toggle span {
  font-weight: 500;
  color: #555;
}

.filter-mode-buttons {
  display: flex;
  gap: 0;
  border-radius: 24px;
  overflow: hidden;
  border: 1px solid #ddd;
  background-color: #f5f5f5;
}

.btn-filter-mode {
  border: none;
  font-size: 14px;
  cursor: pointer;
  color: #666;
  padding: 8px 20px;
  transition: all 0.3s;
  background: none;
  position: relative;
  font-weight: 500;
}

.btn-filter-mode:hover {
  background-color: rgba(255, 165, 0, 0.1);
}

.btn-filter-mode.active {
  background-color: orange;
  color: white;
}
</style>  