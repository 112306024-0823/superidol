<template>
  <div class="page-container">
    <h1 class="page-title">Preferences</h1>
    
    <div class="preferences-container">
      <div class="card">
        <h2 class="card-title">
          <i class="fas fa-cog"></i> General Settings
        </h2>
        
        <div class="form-group">
          <label>Daily Calorie Goal</label>
          <div class="input-with-unit">
            <input type="number" v-model="preferences.calorieGoal" min="1000" max="5000" step="50" class="form-control" />
            <span>kcal</span>
          </div>
        </div>
        
        <div class="form-group">
          <label>Weekly Budget</label>
          <div class="input-with-unit">
            <input type="number" v-model="preferences.weeklyBudget" min="0" step="100" class="form-control" />
            <span>$</span>
          </div>
        </div>
        
        <div class="form-group">
          <label>Language</label>
          <select v-model="preferences.language" class="form-control">
            <option value="en">English</option>
            <option value="zh-TW">繁體中文</option>
          </select>
        </div>
      </div>
      
      <div class="card">
        <h2 class="card-title">
          <i class="fas fa-bell"></i> Notifications
        </h2>
        
        <div class="form-group checkbox-group">
          <label class="checkbox-container">
            <input type="checkbox" v-model="preferences.notifyDailyReminder" />
            <span>Daily meal reminder</span>
          </label>
        </div>
        
        <div class="form-group checkbox-group">
          <label class="checkbox-container">
            <input type="checkbox" v-model="preferences.notifyWeeklyReport" />
            <span>Weekly report notification</span>
          </label>
        </div>
        
        <div class="form-group checkbox-group">
          <label class="checkbox-container">
            <input type="checkbox" v-model="preferences.notifyBudgetAlert" />
            <span>Budget alerts</span>
          </label>
        </div>
      </div>
      
      <div class="card">
        <h2 class="card-title">
          <i class="fas fa-user-shield"></i> Privacy
        </h2>
        
        <div class="form-group checkbox-group">
          <label class="checkbox-container">
            <input type="checkbox" v-model="preferences.shareData" />
            <span>Share anonymous data to improve recommendations</span>
          </label>
        </div>
      </div>
      
      <div class="action-buttons">
        <button class="btn btn-primary" @click="savePreferences">
          <i class="fas fa-save"></i> Save Changes
        </button>
        <button class="btn btn-secondary" @click="resetPreferences">
          <i class="fas fa-undo"></i> Reset to Default
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'UserPreferences',
  setup() {
    const preferences = ref({
      calorieGoal: 2000,
      weeklyBudget: 1000,
      language: 'en',
      notifyDailyReminder: true,
      notifyWeeklyReport: true,
      notifyBudgetAlert: true,
      shareData: false
    })
    
    // Load saved preferences when component mounts
    onMounted(() => {
      loadPreferences()
    })
    
    const loadPreferences = () => {
      // Here you would typically load preferences from backend
      // For now, we'll just use localStorage
      const savedPrefs = localStorage.getItem('userPreferences')
      if (savedPrefs) {
        try {
          const parsedPrefs = JSON.parse(savedPrefs)
          preferences.value = { ...preferences.value, ...parsedPrefs }
        } catch (e) {
          console.error('Error parsing saved preferences', e)
        }
      }
    }
    
    const savePreferences = () => {
      // Here you would typically save to backend
      // For now, we'll just use localStorage
      localStorage.setItem('userPreferences', JSON.stringify(preferences.value))
      
      // Show success message
      ElMessage({
        message: 'Preferences saved successfully!',
        type: 'success',
      })
    }
    
    const resetPreferences = () => {
      preferences.value = {
        calorieGoal: 2000,
        weeklyBudget: 1000,
        language: 'en',
        notifyDailyReminder: true,
        notifyWeeklyReport: true,
        notifyBudgetAlert: true,
        shareData: false
      }
      
      // Show info message
      ElMessage({
        message: 'Preferences reset to default values',
        type: 'info',
      })
    }
    
    return {
      preferences,
      savePreferences,
      resetPreferences
    }
  }
}
</script>

<style scoped>
.page-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  margin-bottom: 30px;
  font-size: 28px;
  color: #333;
  border-bottom: 2px solid #f0f0f0;
  padding-bottom: 10px;
}

.preferences-container {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 20px;
}

.card-title {
  font-size: 18px;
  margin-bottom: 20px;
  color: #333;
  display: flex;
  align-items: center;
  gap: 10px;
}

.card-title i {
  color: #ff7f2a;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.form-control {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 15px;
  transition: border-color 0.3s;
}

.form-control:focus {
  border-color: #ff7f2a;
  outline: none;
  box-shadow: 0 0 0 2px rgba(255, 127, 42, 0.2);
}

.input-with-unit {
  display: flex;
  align-items: center;
}

.input-with-unit input {
  flex: 1;
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}

.input-with-unit span {
  background-color: #f5f5f5;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-left: none;
  border-top-right-radius: 6px;
  border-bottom-right-radius: 6px;
  color: #666;
}

.checkbox-group {
  margin-bottom: 15px;
}

.checkbox-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  user-select: none;
}

.checkbox-container input {
  margin-right: 10px;
  cursor: pointer;
}

.action-buttons {
  display: flex;
  gap: 15px;
  margin-top: 20px;
}

.btn {
  padding: 10px 20px;
  border-radius: 6px;
  border: none;
  font-weight: 500;
  font-size: 15px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.btn-primary {
  background-color: #ff7f2a;
  color: white;
}

.btn-primary:hover {
  background-color: #e86d1f;
}

.btn-secondary {
  background-color: #f3f3f3;
  color: #555;
}

.btn-secondary:hover {
  background-color: #e5e5e5;
}

@media (max-width: 600px) {
  .action-buttons {
    flex-direction: column;
  }
  
  .btn {
    width: 100%;
    justify-content: center;
  }
}
</style> 