<template>
  <div class="weekly-report-page">
    <div class="container">
      <h1 class="page-title">
        <!-- <el-icon><DataAnalysis /></el-icon> --> 健康報告
      </h1>

      <!-- 新增：報告類型選擇器 -->
      <div class="report-type-selector">
        <button
          :class="['btn', currentReportType === 'daily' ? 'btn-primary' : 'btn-secondary']"
          @click="changeReportType('daily')">
          <!-- <el-icon><Calendar /></el-icon>  -->日報告
        </button>
        <button
          :class="['btn', currentReportType === 'weekly' ? 'btn-primary' : 'btn-secondary']"
          @click="changeReportType('weekly')">
          <!-- <el-icon><Collection /></el-icon>  -->週報告
        </button>
        <!-- TODO: 月報告按鈕 -->
      </div>

      <!-- 日期/週次選擇器 -->
      <div class="time-selector">
        <button class="btn btn-icon" @click="changePeriod(-1)">
          <!-- <el-icon><ArrowLeftBold /></el-icon> -->
          <i class="icon-left-arrow">←</i> <!-- 暫用文字替代圖標 -->
        </button>
        <h2 class="current-period-text">{{ reportDateText }}</h2>
        <button class="btn btn-icon" @click="changePeriod(1)">
          <!-- <el-icon><ArrowRightBold /></el-icon> -->
          <i class="icon-right-arrow">→</i> <!-- 暫用文字替代圖標 -->
        </button>
      </div>

      <!-- 日曆選擇器 -->
      <div class="calendar-selector-container" v-if="currentReportType === 'weekly' || currentReportType === 'daily'">
         <Datepicker
            v-model="selectedDateForPicker"
            :inline="true"
            :week-start="0"
            @update:model-value="onDatePicked"
            :enable-time-picker="false"
            placeholder="選擇日期"
            />
      </div>


      <!-- 摘要 (period-summary) -->
      <div class="period-summary" v-if="reportData">
        <div class="summary-row">
          <div class="summary-card">
            <div class="summary-title">
              <!-- <el-icon><Food /></el-icon>  -->卡路里攝取
            </div>
            <div class="summary-value">{{ periodSummary.totalCaloriesIntake }} <span class="unit">大卡</span></div>
            <div class="summary-description" v-if="currentReportType === 'weekly'">
              平均每日: {{ periodSummary.avgDailyCaloriesIntake }} <span class="unit-small">大卡</span>
            </div>
            <div class="summary-description">
              目標: {{ userGoals.daily_calories }} <span class="unit-small">大卡/天</span>
            </div>
          </div>

          <div class="summary-card">
            <div class="summary-title">
              <!-- <el-icon><MostlyCloudy /></el-icon>  -->卡路里消耗
            </div>
            <div class="summary-value">{{ periodSummary.totalCaloriesBurned }} <span class="unit">大卡</span></div>
             <div class="summary-description" v-if="currentReportType === 'weekly'">
              平均每日: {{ periodSummary.avgDailyCaloriesBurned }} <span class="unit-small">大卡</span>
            </div>
            <div class="summary-description">
              {{ periodSummary.exerciseCount }} 次運動
            </div>
          </div>

          <div class="summary-card">
            <div class="summary-title">
             <!-- <el-icon><Timer /></el-icon>  -->運動時長
            </div>
            <div class="summary-value">{{ periodSummary.total_exercise_duration_minutes }} <span class="unit">分鐘</span></div>
            <div class="summary-description" v-if="currentReportType === 'weekly'">
              平均每日: {{ periodSummary.avgDailyExerciseDurationMinutes }} <span class="unit-small">分鐘</span>
            </div>
          </div>

          <div class="summary-card">
            <div class="summary-title">
              <!-- <el-icon><Money /></el-icon>  -->總支出
            </div>
            <div class="summary-value">{{ periodSummary.totalFoodExpense }} <span class="unit">元</span></div>
            <div class="summary-description">
              記錄 {{ periodSummary.foodDaysLogged }}/{{ reportData.report_info.num_days_in_period }} 天
            </div>
          </div>
        </div>
      </div>
      <div v-else-if="isLoading" class="loading-state">
        <!-- <el-icon class="is-loading"><Loading /></el-icon> -->
        載入報告中...
      </div>


      <!-- 圖表區段 -->
      <div class="report-section-row" v-if="reportData">
        <div class="report-section full-width-section">
          <h2 class="section-title">
            <!-- <el-icon><TrendCharts /></el-icon> --> 卡路里趨勢
          </h2>
          <div class="chart-placeholder chart">
            <div class="chart-container">
              <canvas ref="calorieChartEl" id="calorieChart"></canvas>
            </div>
          </div>
        </div>
      </div>

      <div class="report-sections-row-grid" v-if="reportData">
        <div class="report-section">
          <h2 class="section-title">
            <!-- <el-icon><Present /></el-icon>  -->運動紀錄
          </h2>
          <div class="chart-placeholder">
            <div class="chart-container">
              <canvas ref="exerciseTrendChartEl" id="exerciseTrendChart"></canvas>
            </div>
          </div>
        </div>

        <div class="report-section">
          <h2 class="section-title">
            <!-- <el-icon><Tickets /></el-icon>  -->支出紀錄
          </h2>
          <div class="chart-placeholder">
            <div class="chart-container">
              <canvas ref="expenseChartEl" id="expenseChart"></canvas>
            </div>
          </div>
        </div>
      </div>

      <div class="report-section full-width-section" v-if="reportData">
        <h2 class="section-title">
          <!-- <el-icon><Opportunity /></el-icon>  -->建議與提示
        </h2>
        <div class="suggestion-card">
          <p v-if="reportData.suggestions && reportData.suggestions.length > 0">
            根據您這{{ currentReportType === 'daily' ? '日' : '週' }}的飲食和運動記錄，我們有以下建議：
          </p>
          <ul class="suggestion-list" v-if="reportData.suggestions && reportData.suggestions.length > 0">
            <li v-for="(suggestion, index) in reportData.suggestions" :key="index">
             <!-- <el-icon><Star /></el-icon>  -->{{ suggestion }}
            </li>
          </ul>
           <p v-else>
            <!-- <el-icon><InfoFilled /></el-icon>  -->暫無特別建議，請繼續保持記錄！
           </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, watch, nextTick } from 'vue' // Removed watchEffect as it's not used
import { Chart } from 'chart.js/auto'
import Datepicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'
import { ElMessage } from 'element-plus'
// 準備引入圖示，如果已安裝 Element Plus Icons
// import { DataAnalysis, Calendar, Collection, ArrowLeftBold, ArrowRightBold, Food, MostlyCloudy, Timer, Money, Loading, TrendCharts, Present, Tickets, Opportunity, Star, InfoFilled } from '@element-plus/icons-vue'


export default {
  name: 'SummaryReportPage',
  components: {
    Datepicker,
    // 如果使用 Element Plus Icons，在此註冊
    // ElIcon, DataAnalysis, Calendar, Collection, ArrowLeftBold, ArrowRightBold, Food, MostlyCloudy, Timer, Money, Loading, TrendCharts, Present, Tickets, Opportunity, Star, InfoFilled
  },
  setup() {
    const currentReportType = ref('weekly')
    const selectedDateForPicker = ref(new Date())
    const targetDate = ref(new Date())
    const reportData = ref(null)
    const isLoading = ref(false)

    const calorieChartEl = ref(null);
    const exerciseTrendChartEl = ref(null);
    const expenseChartEl = ref(null);

    const initializeTargetDate = () => {
      targetDate.value = new Date()
      selectedDateForPicker.value = new Date(targetDate.value)
    }

    const fetchSummaryReport = async () => {
      isLoading.value = true
      reportData.value = null
      destroyCharts();
      try {
        const userId = localStorage.getItem('userId')
        if (!userId) {
          ElMessage.warning('請先登入以查看報告')
          isLoading.value = false
          return
        }

        let startDateStr = ''
        if (currentReportType.value === 'daily') {
          startDateStr = targetDate.value.toISOString().split('T')[0]
        } else if (currentReportType.value === 'weekly') {
          startDateStr = targetDate.value.toISOString().split('T')[0]
        }

        const apiUrl = `/api/reports/summary?user_id=${userId}&report_type=${currentReportType.value}&start_date=${startDateStr}`
        const response = await fetch(apiUrl)
        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}))
          throw new Error(`API 請求失敗: ${response.status} - ${errorData.error || response.statusText}`)
        }
        const data = await response.json()
        reportData.value = data
      } catch (error) {
        console.error('載入摘要報告數據失敗:', error)
        ElMessage.error(error.message || '載入摘要報告數據失敗，請稍後再試')
        reportData.value = null;
      } finally {
        isLoading.value = false
      }
    }

    const userGoals = computed(() => {
      return reportData.value?.user_goals || {
        daily_calories: 2000,
        daily_budget: 0,
      }
    })

    const reportDateText = computed(() => {
      if (!reportData.value || !reportData.value.report_info) {
        if (currentReportType.value === 'daily') {
            return targetDate.value.toLocaleDateString('zh-TW', { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' });
        } else if (currentReportType.value === 'weekly') {
            const start = new Date(targetDate.value);
            const dayOfWeek = start.getDay() === 0 ? 6 : start.getDay() -1;
            start.setDate(start.getDate() - dayOfWeek);
            const end = new Date(start);
            end.setDate(start.getDate() + 6);
            const startText = start.toLocaleDateString('zh-TW', { month: 'long', day: 'numeric' });
            const endText = end.toLocaleDateString('zh-TW', { month: 'long', day: 'numeric' });
            return `${startText} - ${endText}`;
        }
        return '選擇日期';
      }
      const { actual_start_date, actual_end_date } = reportData.value.report_info
      const startDate = new Date(actual_start_date + 'T00:00:00')
      const endDate = new Date(actual_end_date + 'T00:00:00')

      if (currentReportType.value === 'daily') {
        return startDate.toLocaleDateString('zh-TW', { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' })
      } else if (currentReportType.value === 'weekly') {
        const startText = startDate.toLocaleDateString('zh-TW', { month: 'long', day: 'numeric' })
        const endText = endDate.toLocaleDateString('zh-TW', { month: 'long', day: 'numeric' })
        return `${startText} - ${endText}`
      }
      return '日期範圍'
    })

    const periodSummary = computed(() => {
      const summary = reportData.value?.period_summary
      const reportInfo = reportData.value?.report_info
      const numDays = reportInfo?.num_days_in_period > 0 ? reportInfo.num_days_in_period : 1; // Avoid division by zero

      return {
        totalCaloriesIntake: summary?.total_calories_intake || 0,
        totalCaloriesBurned: summary?.total_calories_burned || 0,
        foodDaysLogged: summary?.food_days_logged || 0,
        totalFoodExpense: summary?.total_food_expense || 0,
        exerciseCount: summary?.exercise_count || 0,
        total_exercise_duration_minutes: summary?.total_exercise_duration_minutes || 0,
        avgDailyCaloriesIntake: Math.round((summary?.total_calories_intake || 0) / numDays),
        avgDailyCaloriesBurned: Math.round((summary?.total_calories_burned || 0) / numDays),
        avgDailyExerciseDurationMinutes: Math.round((summary?.total_exercise_duration_minutes || 0) / numDays),
      }
    })

    const changeReportType = (newType) => {
      currentReportType.value = newType
      fetchSummaryReport()
    }

    const changePeriod = (direction) => {
      const newDate = new Date(targetDate.value)
      if (currentReportType.value === 'daily') {
        newDate.setDate(newDate.getDate() + direction)
      } else if (currentReportType.value === 'weekly') {
        newDate.setDate(newDate.getDate() + direction * 7)
      }
      targetDate.value = newDate
      selectedDateForPicker.value = new Date(newDate)
      fetchSummaryReport()
    }

    const onDatePicked = (date) => {
      if (!date) return;
      targetDate.value = new Date(date)
      selectedDateForPicker.value = new Date(date)
      fetchSummaryReport()
    }

    let calorieChartInstance = null
    let exerciseTrendChartInstance = null
    let expenseChartInstance = null

    const destroyCharts = () => {
        if (calorieChartInstance) calorieChartInstance.destroy(); calorieChartInstance = null;
        if (exerciseTrendChartInstance) exerciseTrendChartInstance.destroy(); exerciseTrendChartInstance = null;
        if (expenseChartInstance) expenseChartInstance.destroy(); expenseChartInstance = null;
    }

    const initOrUpdateCharts = (dailyTrends) => {
      if (!dailyTrends || dailyTrends.length === 0) {
        destroyCharts();
        return;
      }

      const labels = dailyTrends.map(t => {
        const dateObj = new Date(t.date + 'T00:00:00');
        return dateObj.toLocaleDateString('zh-TW', { month: 'numeric', day: 'numeric', weekday: 'short' });
      });

      const chartOptionsBase = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'top' }, tooltip: { mode: 'index', intersect: false }},
        interaction: { mode: 'index', intersect: false },
      };

      // Calorie Chart
      const intakeData = dailyTrends.map(t => t.calories_intake);
      const burnedData = dailyTrends.map(t => t.calories_burned);
      const netData = dailyTrends.map(t => t.calories_intake - t.calories_burned);

      if (calorieChartEl.value) { // Ensure canvas element is available
        if (calorieChartInstance) {
          calorieChartInstance.data.labels = labels;
          calorieChartInstance.data.datasets[0].data = intakeData;
          calorieChartInstance.data.datasets[1].data = burnedData;
          calorieChartInstance.data.datasets[2].data = netData;
          calorieChartInstance.update();
        } else {
          calorieChartInstance = new Chart(calorieChartEl.value, {
            type: 'bar',
            data: { labels, datasets: [
                { type: 'bar', label: '卡路里攝取', data: intakeData, backgroundColor: 'rgba(66, 165, 245, 0.7)', borderColor: '#42a5f5', order: 2 },
                { type: 'bar', label: '卡路里消耗', data: burnedData, backgroundColor: 'rgba(102, 187, 106, 0.7)', borderColor: '#66bb6a', order: 3 },
                { type: 'line', label: '淨卡路里', data: netData, borderColor: '#ff7043', backgroundColor: 'rgba(255, 112, 67, 0.1)', borderWidth: 2, tension: 0.3, yAxisID: 'y', order: 1, pointBackgroundColor: '#ff7043' }
            ]},
            options: { ...chartOptionsBase, scales: { y: { beginAtZero: true, title: { display: true, text: '卡路里' }}, x: {title: {display: dailyTrends.length > 1, text: '日期' }} }}
          });
        }
      }


      // Exercise Trend Chart
      const exerciseDurationData = dailyTrends.map(t => t.exercise_duration_minutes);
      if (exerciseTrendChartEl.value) { // Ensure canvas element is available
        if (exerciseTrendChartInstance) {
          exerciseTrendChartInstance.data.labels = labels;
          exerciseTrendChartInstance.data.datasets[0].data = exerciseDurationData;
          exerciseTrendChartInstance.update();
        } else {
           exerciseTrendChartInstance = new Chart(exerciseTrendChartEl.value, {
              type: 'line',
              data: { labels, datasets: [{ label: '運動時間 (分鐘)', data: exerciseDurationData, borderColor: '#42a5f5', backgroundColor: 'rgba(66, 165, 245, 0.2)', fill: true, tension: 0.3, pointBackgroundColor: '#42a5f5' }]},
              options: { ...chartOptionsBase, scales: { y: { beginAtZero: true, title: { display: true, text: '時間 (分鐘)' }}, x: { title: { display: dailyTrends.length > 1, text: '日期' }} }}
          });
        }
      }


      // Expense Chart
      const expenseData = dailyTrends.map(t => t.food_expense);
      if (expenseChartEl.value) { // Ensure canvas element is available
        if (expenseChartInstance) {
          expenseChartInstance.data.labels = labels;
          expenseChartInstance.data.datasets[0].data = expenseData;
          expenseChartInstance.update();
        } else {
          expenseChartInstance = new Chart(expenseChartEl.value, {
              type: 'bar',
              data: { labels, datasets: [{ label: '每日支出 (元)', data: expenseData, backgroundColor: 'rgba(255, 202, 40, 0.7)', borderColor: '#ffca28', borderRadius: 4 }]},
              options: { ...chartOptionsBase, scales: { y: { beginAtZero: true, title: { display: true, text: '元' }}, x: { title: { display: dailyTrends.length > 1, text: '日期' }} }}
          });
        }
      }
    }

    onMounted(() => {
      initializeTargetDate()
      fetchSummaryReport()
    })

    watch(() => reportData.value, async (newData, oldData) => {
      if (newData && newData.daily_trends) {
         await nextTick();
         initOrUpdateCharts(newData.daily_trends)
      } else if (!newData && oldData) {
        destroyCharts()
      }
    }, { deep: true })


    return {
      currentReportType,
      selectedDateForPicker,
      targetDate,
      reportData,
      isLoading,
      userGoals,
      reportDateText,
      periodSummary,
      changeReportType,
      changePeriod,
      onDatePicked,
      calorieChartEl,
      exerciseTrendChartEl,
      expenseChartEl,
    }
  }
}
</script>

<style scoped>
/* ----- 全局變量 (理想情況下在 main.css 或 App.vue style) ----- */
:root {
  --primary-color: #409EFF; /* Element Plus 主色藍 */
  --primary-color-dark: #337ecc;
  --success-color: #67C23A;
  --warning-color: #E6A23C;
  --danger-color: #F56C6C;
  --info-color: #909399;
  --text-primary: #303133;
  --text-regular: #606266;
  --text-secondary: #909399;
  --border-color-light: #e4e7ed;
  --bg-color: #f5f7fa;
}

/* ----- 整體與間距 ----- */
.weekly-report-page .container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', Arial, sans-serif;
}

.page-title {
  font-size: 2.25rem; /* 36px */
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 30px;
  text-align: center;
  display: flex;
  align-items: center;
  justify-content: center;
}
.page-title .el-icon {
  margin-right: 10px;
  font-size: 2.5rem;
}

.report-type-selector,
.time-selector,
.calendar-selector-container,
.period-summary,
.report-section-row,
.report-sections-row-grid, /* Changed class name */
.report-section {
  margin-bottom: 30px;
}

/* ----- 按鈕 ----- */
.report-type-selector {
  display: flex;
  justify-content: center;
  gap: 15px; /* 按鈕間距 */
  margin-bottom: 25px;
}
.btn {
  padding: 10px 20px;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 500;
  transition: all 0.2s ease;
  border: 1px solid transparent;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px; /* 圖標與文字間距 */
}
.btn .el-icon {
  font-size: 1.1em;
}

.btn-primary {
  background-color: var(--primary-color);
  color: white;
  border-color: var(--primary-color);
}
.btn-primary:hover {
  background-color: var(--primary-color-dark);
  border-color: var(--primary-color-dark);
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.btn-secondary {
  background-color: #f0f2f5;
  color: var(--text-regular);
  border-color: #dcdfe6;
}
.btn-secondary:hover {
  background-color: #e4e7ed;
  border-color: #c8c9cc;
  color: var(--primary-color);
}

.time-selector {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}
.current-period-text {
  font-size: 1.5rem;
  font-weight: 500;
  color: var(--text-primary);
  margin: 0 20px;
  min-width: 200px; /* 給定最小寬度避免跳動 */
  text-align: center;
}
.btn-icon {
  background: transparent;
  border: none;
  padding: 8px;
  color: var(--primary-color);
  cursor: pointer;
}
.btn-icon .el-icon, .btn-icon i {
  font-size: 1.8rem; /* 調整圖標大小 */
}
.btn-icon:hover {
  color: var(--primary-color-dark);
}

/* ----- 日曆選擇器 ----- */
.calendar-selector-container {
  display: flex;
  justify-content: center;
  max-width: 360px; /* 限制日曆寬度 */
  margin-left: auto;
  margin-right: auto;
}

/* ----- 摘要卡片 ----- */
.summary-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); /* 響應式卡片 */
  gap: 20px;
}
.summary-card {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 6px 16px -8px rgba(0,0,0,.08), 0 9px 28px 0 rgba(0,0,0,.05), 0 12px 48px 16px rgba(0,0,0,.03);
  border: 1px solid var(--border-color-light);
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}
.summary-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px -6px rgba(0,0,0,.1), 0 12px 32px 0 rgba(0,0,0,.07), 0 16px 52px 18px rgba(0,0,0,.04);
}
.summary-title {
  font-size: 0.9rem;
  color: var(--text-secondary);
  margin-bottom: 8px;
  font-weight: 500;
  display: flex;
  align-items: center;
}
.summary-title .el-icon {
  margin-right: 6px;
  color: var(--text-secondary);
}
.summary-value {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
  line-height: 1.2;
  display: flex;
  align-items: baseline;
}
.summary-value .unit {
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--text-secondary);
  margin-left: 6px;
}
.summary-description {
  font-size: 0.85rem;
  color: var(--text-regular);
}
.summary-description .unit-small {
   font-size: 0.8rem;
   color: var(--text-secondary);
}


/* ----- 區塊標題 ----- */
.report-section {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 6px 16px -8px rgba(0,0,0,.08), 0 9px 28px 0 rgba(0,0,0,.05), 0 12px 48px 16px rgba(0,0,0,.03);
  border: 1px solid var(--border-color-light);
}
.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-color-light);
  display: flex;
  align-items: center;
}
.section-title .el-icon {
  margin-right: 8px;
  color: var(--primary-color);
}
.full-width-section { /* 用於單獨佔一行的區塊 */
  grid-column: 1 / -1; /* 如果父容器是 grid */
}

/* ----- 圖表區塊網格佈局 ----- */
.report-sections-row-grid {
  display: grid;
  grid-template-columns: 1fr 1fr; /* 預設兩欄 */
  gap: 20px;
}

/* ----- 圖表容器 ----- */
.chart-container {
  height: 350px;
  position: relative; /* For Chart.js responsiveness */
}
.chart-placeholder { /* 包裹 canvas 的 div */
  width: 100%;
  height: 100%;
}


/* ----- 建議區塊 ----- */
.suggestion-card {
   background-color: var(--bg-color);
   border-left: 4px solid var(--primary-color);
   padding: 20px;
   border-radius: 8px;
   margin-top: 10px; /* 與標題間距 */
}
.suggestion-card p {
  color: var(--text-regular);
  line-height: 1.7;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
}
.suggestion-card p .el-icon {
  margin-right: 8px;
  color: var(--info-color);
  font-size: 1.2em;
}
.suggestion-list {
  list-style: none;
  padding-left: 0;
}
.suggestion-list li {
  color: var(--text-regular);
  line-height: 1.8;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}
.suggestion-list li .el-icon {
  margin-right: 8px;
  color: var(--warning-color); /* 或 var(--success-color) */
  font-size: 1.1em;
}


/* ----- Loading 狀態 ----- */
.loading-state {
  display: flex;
  flex-direction: column; /* 讓圖標和文字垂直排列 */
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
  font-size: 1.1rem;
  color: var(--text-secondary);
}
.loading-state .el-icon {
  font-size: 2.5rem;
  margin-bottom: 15px;
  color: var(--primary-color);
}
/* Element Plus is-loading class already handles animation */


/* ----- 響應式調整 ----- */
@media (max-width: 992px) {
  .report-sections-row-grid {
    grid-template-columns: 1fr; /* 中螢幕變單欄 */
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: 1.8rem;
  }
  .summary-row {
    grid-template-columns: 1fr; /* 小螢幕摘要卡片堆疊 */
  }
  .current-period-text {
    font-size: 1.2rem;
    min-width: 150px;
  }
  .btn {
    padding: 8px 15px;
    font-size: 0.9rem;
  }
  .section-title {
    font-size: 1.3rem;
  }
  .chart-container {
    height: 300px; /* 稍微降低圖表高度 */
  }
}

@media (max-width: 480px) {
  .container {
    padding: 15px;
  }
  .report-type-selector {
    flex-direction: column; /* 更小螢幕時按鈕垂直排列 */
    gap: 10px;
  }
  .time-selector {
    flex-wrap: wrap; /* 允許換行 */
  }
  .current-period-text {
     order: -1; /* 將日期文字提到最前 */
     width: 100%;
     margin-bottom: 10px;
  }
  .page-title .el-icon {
    font-size: 2rem;
  }
}
</style>




