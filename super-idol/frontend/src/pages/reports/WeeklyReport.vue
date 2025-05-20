<template>
  <div class="weekly-report-page">
    <div class="container">
      <h1 class="page-title">每週報告</h1>

      <!-- 週次選擇器 -->
      <div class="week-selector">
        <button class="btn btn-icon" @click="changeWeek(-1)">
          <i class="icon-left-arrow"></i>
        </button>
        <h2 class="current-week">{{ weekRangeText }}</h2>
        <button class="btn btn-icon" @click="changeWeek(1)">
          <i class="icon-right-arrow"></i>
        </button>
      </div>



      <!-- 每週摘要 -->
      <div class="weekly-summary">
        <div class="summary-row">
          <div class="summary-card">
            <div class="summary-title">平均每日卡路里</div>
            <div class="summary-value">{{ weeklySummary.avgCaloriesPerDay }}</div>
            <div class="summary-description">
              目標: {{ userGoals.dailyCalories }} 卡路里/天
            </div>
          </div>

          <div class="summary-card">
            <div class="summary-title">卡路里消耗</div>
            <div class="summary-value">{{ weeklySummary.totalCaloriesBurned }}</div>
            <div class="summary-description">
              {{ weeklySummary.exerciseCount }} 次運動記錄
            </div>
          </div>

          <div class="summary-card">
            <div class="summary-title">飲食記錄完成度</div>
            <div class="summary-value">{{ weeklySummary.completionRate }}%</div>
            <div class="summary-description">
              記錄 {{ weeklySummary.daysLogged }}/7 天
            </div>
          </div>
        </div>
      </div>

      <!-- 月曆 -->
      <div class="report-section">
        <h2 class="section-title">月曆記錄</h2>
        <div class="calendar">
          <!-- TODO: 實現月曆 -->

          <div class="chart-placeholder">

            <!-- 月曆選擇器 -->
            <div class="calendar-container">
              <Datepicker v-model="selectedDate" @update:model-value="onDateSelected" :inline="true" />
            </div>
          </div>
        </div>
      </div>

      <!-- 卡路里趨勢圖 -->
      <div class="report-section">
        <h2 class="section-title">卡路里趨勢</h2>
        <div class="chart-container">
          <!-- TODO: 實現卡路里趨勢圖 -->
          <div class="chart-placeholder">
            <div class="chart-container">
              <canvas id="calorieChart"></canvas>
            </div>
            <!--<p>卡路里趨勢圖將在此顯示</p>-->
          </div>
        </div>
      </div>

      <!-- 營養素分佈 -->
      <div class="report-section">
        <h2 class="section-title">營養素分佈</h2>
        <div class="chart-container">
          <!-- TODO: 實現營養素分佈圖 -->
          <div class="chart-placeholder">
            <p>營養素分佈圖將在此顯示</p>
          </div>
        </div>
      </div>

      <!-- 每餐分佈 -->
      <div class="report-section">
        <h2 class="section-title">每餐分佈</h2>
        <div class="chart-container">
          <!-- TODO: 實現每餐分佈圖 -->
          <div class="chart-placeholder">
            <p>每餐分佈圖將在此顯示</p>
          </div>
        </div>
      </div>

      <!-- 運動記錄摘要 -->
      <div class="report-section">
        <h2 class="section-title">運動記錄</h2>
        <div class="exercise-summary">
          <!-- TODO: 實現運動記錄摘要 -->
          <div class="chart-placeholder">
            <p>運動記錄摘要將在此顯示</p>
          </div>
        </div>
      </div>



      <!-- 建議與提示 -->
      <div class="report-section">
        <h2 class="section-title">建議與提示</h2>
        <div class="suggestion-card">
          <!-- TODO: 實現根據用戶數據生成的建議 -->
          <p>根據您這週的飲食和運動記錄，我們有以下建議：</p>
          <ul class="suggestion-list">
            <li>嘗試增加蛋白質攝取，您的蛋白質攝取略低於建議值。</li>
            <li>每週至少進行3次30分鐘以上的有氧運動。</li>
            <li>建議減少加工食品的攝取，增加新鮮蔬果比例。</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
// TODO: 導入相關 store、工具函數和圖表庫
import { Chart } from 'chart.js/auto'
import Datepicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'

export default {
  name: 'WeeklyReport',
  components: {
    Datepicker
  },
  setup() {
    // 當前選中的週次
    const selectedWeek = ref({
      start: new Date(), // 默認為本週開始
      end: new Date()    // 默認為本週結束
    })
    const selectedDate = ref(new Date())

    // 設置本週的起始和結束時間
    const initializeCurrentWeek = () => {
      const now = new Date()
      const dayOfWeek = now.getDay() // 0 是週日，1 是週一，以此類推
      const diff = now.getDate() - dayOfWeek

      // 設置本週的起始時間（週日）
      selectedWeek.value.start = new Date(now.setDate(diff))

      // 設置本週的結束時間（週六）
      selectedWeek.value.end = new Date(now)
      selectedWeek.value.end.setDate(selectedWeek.value.start.getDate() + 6)
    }

    // 用戶目標（實際應從用戶設置獲取）
    const userGoals = ref({
      dailyCalories: 2000,
      protein: 150,
      carbs: 200,
      fat: 65
    })

    // 格式化週次範圍文字
    const weekRangeText = computed(() => {
      const startText = selectedWeek.value.start.toLocaleDateString('zh-TW', {
        month: 'long',
        day: 'numeric'
      })

      const endText = selectedWeek.value.end.toLocaleDateString('zh-TW', {
        month: 'long',
        day: 'numeric'
      })

      return `${startText} - ${endText}`
    })

    // 週報摘要數據
    const weeklySummary = ref({
      avgCaloriesPerDay: 1850,
      totalCaloriesBurned: 1200,
      exerciseCount: 5,
      completionRate: 85,
      daysLogged: 6,
      avgProtein: 120,
      avgCarbs: 180,
      avgFat: 60
    })

    // 變更週次
    const changeWeek = (direction) => {
      const newStart = new Date(selectedWeek.value.start)
      const newEnd = new Date(selectedWeek.value.end)

      // 向前或向後一週
      newStart.setDate(newStart.getDate() + (direction * 7))
      newEnd.setDate(newEnd.getDate() + (direction * 7))

      selectedWeek.value = {
        start: newStart,
        end: newEnd
      }

      // 加載所選週次的報告數據
      loadWeeklyData()
    }

    const onDateSelected = (date) => {
      const selected = new Date(date)
      const dayOfWeek = selected.getDay()
      const startOfWeek = new Date(selected)
      startOfWeek.setDate(selected.getDate() - dayOfWeek)

      const endOfWeek = new Date(startOfWeek)
      endOfWeek.setDate(startOfWeek.getDate() + 6)

      selectedWeek.value = { start: startOfWeek, end: endOfWeek }
      selectedDate.value = selected
      loadWeeklyData()
    }

    // 加載週報數據
    const loadWeeklyData = async () => {
      // TODO: 從API獲取所選週次的報告數據
      console.log('加載週次', weekRangeText.value, '的報告數據')

      // 模擬數據加載
      // weeklySummary.value = ...


    }
    // TODO: 宣告圖表數據
    const calorieTrendData = ref({
      labels: ['週日', '週一', '週二', '週三', '週四', '週五', '週六'],
      datasets: [
        {
          label: '實際攝取',
          data: [1800, 2000, 1900, 1850, 1750, 2100, 1950],
          borderColor: '#42a5f5',
          fill: false,
        },
        {
          label: '目標攝取',
          data: [2000, 2000, 2000, 2000, 2000, 2000, 2000],
          borderColor: '#66bb6a',
          borderDash: [5, 5],
          fill: false,
        }
      ]
    })

    // 初始化
    onMounted(() => {
      initializeCurrentWeek()
      loadWeeklyData()
      //宣告圖表
      new Chart(document.getElementById('calorieChart'), {
        type: 'line',
        data: calorieTrendData.value,
        options: {
          responsive: true,
          plugins: { legend: { position: 'top' } }
        }
      })
    })

    return {
      selectedWeek,
      selectedDate,
      weekRangeText,
      userGoals,
      weeklySummary,
      changeWeek,
      onDateSelected
    }
  }
}
</script>

<style scoped>
.weekly-report-page {
  padding: 20px 0;
}

.page-title {
  margin-bottom: 24px;
  font-size: 28px;
  color: var(--text-color);
}

.week-selector {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
}

.current-week {
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

.weekly-summary {
  margin-bottom: 32px;
}

.summary-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.summary-card {
  background-color: var(--card-bg);
  border-radius: 8px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.summary-title {
  font-size: 16px;
  color: #666;
  margin-bottom: 8px;
}

.summary-value {
  font-size: 28px;
  font-weight: bold;
  color: var(--primary-color);
  margin-bottom: 8px;
}

.summary-description {
  font-size: 14px;
  color: #888;
}

.report-section {
  background-color: var(--card-bg);
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.section-title {
  margin-top: 0;
  margin-bottom: 16px;
  font-size: 20px;
  color: var(--text-color);
}

.chart-container {
  height: 300px;
  width: 100%;
}

.chart-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.02);
  border-radius: 8px;
  color: #888;
}

.suggestion-list {
  padding-left: 20px;
  margin-top: 12px;
}

.suggestion-list li {
  margin-bottom: 8px;
  color: #555;
}

@media (max-width: 768px) {
  .summary-row {
    grid-template-columns: 1fr;
  }

  .chart-container {
    height: 250px;
  }
}
</style>