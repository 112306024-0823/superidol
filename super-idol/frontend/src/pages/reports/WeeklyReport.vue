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
            <div class="summary-title">卡路里攝取</div>
            <div class="summary-value">{{ weeklySummary.totalExpense }}</div>
            <div class="summary-description">
              目標: {{ userGoals.dailyCalories }} 卡路里/天
            </div>
          </div>


          <div class="summary-card">
            <div class="summary-title">卡路里消耗</div>
            <div class="summary-value">{{ weeklySummary.completionRate }}%</div>
            <div class="summary-description">
              記錄 {{ weeklySummary.daysLogged }}/7 天
            </div>
          </div>


          <div class="summary-card">
            <div class="summary-title">運動時間</div>
            <div class="summary-value">{{ weeklySummary.totalCaloriesBurned }}</div>
            <div class="summary-description">
              {{ weeklySummary.exerciseCount }} 次運動記錄
            </div>
          </div>


          <div class="summary-card">
            <div class="summary-title">總支出</div>
            <div class="summary-value">{{ weeklySummary.totalExpense }}</div>
            <div class="summary-description">
              目標: {{ userGoals.dailyCalories }} 卡路里/天
            </div>
          </div>
        </div>
      </div>


      <div class="report-section-row">
        <div class="report-section">
          <h2 class="section-title">日期選取 & 卡路里趨勢</h2>


          <div class="date-calorie-row">
            <div class="calendar-container chart">
              <Datepicker v-model="selectedDate" :inline="true" :week-start="0" @update:model-value="onDateSelected" />
            </div>


            <div class="chart-placeholder chart">
              <div class="chart-container">
                <canvas id="calorieChart"></canvas>
              </div>
            </div>
          </div>
        </div>
      </div>




      <!-- 把運動紀錄跟支出紀錄包在一個父容器 -->
      <div class="report-sections-row">
        <div class="report-section">
          <h2 class="section-title">運動紀錄</h2>
          <div class="exercise-summary">
            <div class="chart-placeholder">
              <div class="chart-container">
                <canvas id="exerciseTrendChart"></canvas>
              </div>
            </div>
          </div>
        </div>


        <div class="report-section">
          <h2 class="section-title">支出紀錄</h2>
          <div class="chart-container">
            <div class="chart-placeholder">
              <canvas id="expenseChart"></canvas>
            </div>
          </div>
        </div>
      </div>










      <div class="report-section">
        <h2 class="section-title">建議與提示</h2>
        <div class="suggestion-card">
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
import { Chart } from 'chart.js/auto'
import Datepicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'


export default {
  name: 'WeeklyReport',
  components: {
    Datepicker
  },
  setup() {
    const selectedWeek = ref({ start: new Date(), end: new Date() })
    const selectedDate = ref(new Date())


    const initializeCurrentWeek = () => {
      const now = new Date()
      const dayOfWeek = now.getDay() === 0 ? 6 : now.getDay() - 1
      const start = new Date(now)
      start.setDate(now.getDate() - dayOfWeek)
      const end = new Date(start)
      end.setDate(start.getDate() + 6)
      selectedWeek.value = { start, end }
    }




    const userGoals = ref({
      dailyCalories: 2000,
      protein: 150,
      carbs: 200,
      fat: 65
    })


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


    const weeklySummary = ref({
      totalCaloriesBurned: 1200,
      exerciseCount: 5,
      completionRate: 85,
      totalExpense: 750,
      daysLogged: 6,
      avgProtein: 120,
      avgCarbs: 180,
      avgFat: 60
    })


    const changeWeek = (direction) => {
      const newStart = new Date(selectedWeek.value.start)
      const newEnd = new Date(selectedWeek.value.end)
      newStart.setDate(newStart.getDate() + direction * 7)
      newEnd.setDate(newEnd.getDate() + direction * 7)
      selectedWeek.value = { start: newStart, end: newEnd }
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


    const loadWeeklyData = () => {
      console.log('加載週次', weekRangeText.value, '的報告數據')
    }


    onMounted(() => {
      initializeCurrentWeek()
      loadWeeklyData()


      new Chart(document.getElementById('calorieChart'), {
        type: 'bar',
        data: {
          labels: ['週日', '週一', '週二', '週三', '週四', '週五', '週六'],
          datasets: [
            {
              type: 'bar',
              label: '卡路里攝取',
              data: [1800, 2000, 1900, 1850, 1750, 2100, 1950],
              backgroundColor: '#42a5f5',
              order: 2
            },
            {
              type: 'bar',
              label: '卡路里消耗',
              data: [500, 700, 600, 650, 400, 800, 500],
              backgroundColor: '#66bb6a',
              order: 3
            },
            {
              type: 'line',
              label: '淨卡路里',
              data: [1300, 1300, 1300, 1200, 1350, 1300, 1450],
              order: 3,
              borderColor: '#ff7043',
              backgroundColor: '#ff7043',
              borderWidth: 2,
              tension: 0.3,
              yAxisID: 'y',
              order: 1 // 折線在最上層
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: 'top' },
            tooltip: { mode: 'index', intersect: false }
          },
          interaction: { mode: 'index', intersect: false },
          scales: {
            y: {
              beginAtZero: true,
              title: { display: true, text: '卡路里' }
            }
          }
        }


      })
      new Chart(document.getElementById('exerciseTrendChart'), {
        type: 'line',
        data: {
          labels: ['週日', '週一', '週二', '週三', '週四', '週五', '週六'],
          datasets: [
            {
              label: '運動時間 (分鐘)',
              data: [30, 45, 60, 20, 50, 0, 40], // 可依資料更新
              borderColor: '#42a5f5',
              backgroundColor: 'rgba(66, 165, 245, 0.2)',
              fill: true,
              tension: 0.3,
              pointBackgroundColor: '#42a5f5'
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: 'top' },
            tooltip: { mode: 'index', intersect: false }
          },
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: '時間 (分鐘)'
              }
            },
            x: {
              title: {
                display: true,
                text: '星期'
              }
            }
          }
        }
      })


      new Chart(document.getElementById('expenseChart'), {
        type: 'bar',
        data: {
          labels: ['週日', '週一', '週二', '週三', '週四', '週五', '週六'],
          datasets: [
            {
              label: '每日支出 (元)',
              data: [120, 90, 150, 100, 80, 200, 130], // 可依實際資料更新
              backgroundColor: '#ffca28',
              borderRadius: 4
            }
          ]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { position: 'top' },
            tooltip: { mode: 'index', intersect: false }
          },
          scales: {
            y: {
              beginAtZero: true,
              title: { display: true, text: '元' }
            },
            x: {
              title: { display: true, text: '星期' }
            }
          }
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
/* 你的原始樣式保持不變 */
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


.chart-row {
  display: flex;
  justify-content: start;
  gap: 16px;
}


.chart {
  flex: 1;
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


.date-calorie-row {
  display: flex;
  gap: 24px;
  align-items: center;
}


.date-calorie-row>.chart {
  flex: 1;
  min-width: 0;
  /* 防止溢出 */
}


.calendar-container {
  max-width: 350px;
  /* 限制日曆寬度，可自行調整 */
  flex-shrink: 0;
}


.chart-placeholder {
  height: 300px;
}




.report-sections-row {
  display: flex;
  gap: 24px;
  /* 兩個區塊間距 */
  margin-bottom: 24px;
}


.report-sections-row>.report-section {
  flex: 1;
  /* 平均分寬 */
  min-width: 0;
  /* 避免子元素溢出 */
}


/* 手機下改成直排 */
@media (max-width: 768px) {
  .report-sections-row {
    flex-direction: column;
  }
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




