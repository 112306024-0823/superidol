<template>
  <div class="basic-info-page">
    <el-card class="profile-card">
      <div class="profile-header">
        <h2>
          <i class="el-icon-user" style="color:#f08c00;margin-right:8px"></i>
          個人基本資料
        </h2>
        <el-button
          v-if="!isEditing"
          type="warning"
          icon="el-icon-edit"
          @click="startEdit"
          class="edit-btn"
        >編輯</el-button>
              </div>
      <el-divider />
      <!-- 檢視模式 -->
      <template v-if="!isEditing">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="姓名">{{ profile.name }}</el-descriptions-item>
          <el-descriptions-item label="電子郵件">{{ profile.email }}</el-descriptions-item>
          <el-descriptions-item label="每餐預算">{{ profile.budget }}</el-descriptions-item>
          <el-descriptions-item label="每週熱量限制">{{ profile.weekcalorielimit }}</el-descriptions-item>
          <el-descriptions-item label="體重">{{ profile.weight }}</el-descriptions-item>
        </el-descriptions>
        <el-divider />
        <div class="preference-view">
          <div class="pref-block">
            <span class="pref-title">食物偏好：</span>
            <el-tag
              v-for="type in selectedFoodTypes"
              :key="type"
              class="pref-tag food-tag"
              effect="dark"
              style="background:#fff7e6;color:#f08c00;border-color:#f08c00"
            >🍔 {{ type }}</el-tag>
            <span v-if="!selectedFoodTypes.length" class="pref-empty">無</span>
              </div>
          <div class="pref-block">
            <span class="pref-title">運動偏好：</span>
            <el-tag
              v-for="item in selectedExerciseNames"
              :key="item"
              class="pref-tag exercise-tag"
              effect="dark"
              style="background:#fff7e6;color:#f08c00;border-color:#f08c00"
            >🏃‍♂️ {{ item }}</el-tag>
            <span v-if="!selectedExerciseNames.length" class="pref-empty">無</span>
          </div>
          <div class="pref-block">
            <span class="pref-title">餐廳偏好：</span>
            <el-tag
              v-for="id in selectedRestaurantIds"
              :key="id"
              class="pref-tag restaurant-tag"
              effect="dark"
              style="background:#fff7e6;color:#f08c00;border-color:#f08c00"
            >🏠 {{ getRestaurantName(id) }}</el-tag>
            <span v-if="!selectedRestaurantIds.length" class="pref-empty">無</span>
          </div>
            </div>
      </template>
      <!-- 編輯模式 -->
      <template v-else>
        <el-form :model="editProfile" label-width="110px" class="profile-form">
          <el-form-item label="姓名">
            <el-input v-model="editProfile.name" />
          </el-form-item>
          <el-form-item label="電子郵件">
            <el-input v-model="editProfile.email" />
          </el-form-item>
          <el-form-item label="每餐預算">
            <el-input-number v-model="editProfile.budget" :min="0" />
          </el-form-item>
          <el-form-item label="每週熱量限制">
            <el-input-number v-model="editProfile.weekcalorielimit" :min="0" />
          </el-form-item>
          <el-form-item label="體重">
            <el-input-number v-model="editProfile.weight" :min="0" />
          </el-form-item>
        </el-form>
        <el-divider />
        <el-card class="preference-card" shadow="never">
          <div class="preference-header">
            <h3 style="color:#f08c00">食物偏好</h3>
          </div>
          <el-checkbox-group v-model="editSelectedFoodTypes">
            <el-checkbox v-for="type in foodTypes" :key="type.name" :label="type.name">
              <span style="color:#f08c00">🍔</span> {{ type.name }}
            </el-checkbox>
          </el-checkbox-group>
        </el-card>
        <el-card class="preference-card" shadow="never">
          <div class="preference-header">
            <h3 style="color:#f08c00">運動偏好</h3>
          </div>
          <el-checkbox-group v-model="editSelectedExerciseNames">
            <el-checkbox v-for="item in exerciseItems" :key="item.name" :label="item.name">
              <span style="color:#f08c00">🏃‍♂️</span> {{ item.name }}
            </el-checkbox>
          </el-checkbox-group>
        </el-card>
        <el-card class="preference-card" shadow="never">
          <div class="preference-header">
            <h3 style="color:#f08c00">餐廳偏好</h3>
          </div>
          <el-checkbox-group v-model="editSelectedRestaurantIds">
            <el-checkbox v-for="r in restaurants" :key="r.id" :label="r.id">
              <span style="color:#f08c00">🏠</span> {{ r.name }}
            </el-checkbox>
          </el-checkbox-group>
        </el-card>
        <div class="form-actions">
          <el-button type="warning" :loading="isLoading" @click="saveEdit" class="save-btn">儲存</el-button>
          <el-button @click="cancelEdit">取消</el-button>
      </div>
      </template>
      <el-dialog v-model="dialogVisible" title="訊息" width="300">
        <span>{{ dialogMsg }}</span>
        <template #footer>
          <el-button type="primary" @click="dialogVisible = false">確定</el-button>
        </template>
      </el-dialog>
      <el-loading v-if="isLoading" lock text="載入中..." />
    </el-card>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import axios from 'axios'

export default {
  name: 'BasicInfo',
  setup() {
    // 狀態
    const profile = ref({
      name: '',
      email: '',
      budget: null,
      weekcalorielimit: null,
      weight: null
    })
    const isLoading = ref(false)
    const isEditing = ref(false)
    const errorMsg = ref('')
    // 偏好選項
    const foodTypes = ref([])
    const exerciseItems = ref([])
    const restaurants = ref([])
    // 使用者已選偏好
    const selectedFoodTypes = ref([])
    const selectedExerciseNames = ref([])
    const selectedRestaurantIds = ref([])
    // 編輯用暫存
    const editProfile = reactive({
      name: '',
      email: '',
      budget: null,
      weekcalorielimit: null,
      weight: null
    })
    const editSelectedFoodTypes = ref([])
    const editSelectedExerciseNames = ref([])
    const editSelectedRestaurantIds = ref([])
    // dialog
    const dialogVisible = ref(false)
    const dialogMsg = ref('')

    // 載入所有可選項目
    const fetchOptions = async () => {
      const [foodRes, exerciseRes, restaurantRes] = await Promise.all([
        axios.get('/api/food-types'),
        axios.get('/api/exercise-items'),
        axios.get('/api/restaurants')
      ])
      foodTypes.value = foodRes.data
      exerciseItems.value = exerciseRes.data
      restaurants.value = restaurantRes.data
    }

    // 載入目前使用者偏好
    const fetchUserPreferences = async (userId) => {
      try {
        const [foodPref, exercisePref, restaurantPref] = await Promise.all([
          axios.get('/api/user/food-preferences', { params: { user_id: userId } }),
          axios.get('/api/user/exercise-preferences', { params: { user_id: userId } }),
          axios.get('/api/user/restaurant-preferences', { params: { user_id: userId } })
        ])
        selectedFoodTypes.value = foodPref.data.food_types || []
        selectedExerciseNames.value = exercisePref.data.exercise_names || []
        selectedRestaurantIds.value = restaurantPref.data.restaurant_ids || []
      } catch (err) {
        // 若查無偏好可忽略
      }
    }
    
    // 載入個人資料
    const fetchProfile = async () => {
      isLoading.value = true
      errorMsg.value = ''
      try {
        const token = localStorage.getItem('token')
        const res = await axios.get('/api/auth/user', {
          headers: { Authorization: `Bearer ${token}` }
        })
        profile.value.name = res.data.name
        profile.value.email = res.data.email
        profile.value.budget = res.data.budget
        profile.value.weekcalorielimit = res.data.weekCalorieLimit
        profile.value.weight = res.data.weight
      } catch (err) {
        errorMsg.value = err.response?.data?.error || '載入個人資料失敗'
      } finally {
        isLoading.value = false
      }
    }

    // 進入編輯模式
    const startEdit = () => {
      editProfile.name = profile.value.name
      editProfile.email = profile.value.email
      editProfile.budget = profile.value.budget
      editProfile.weekcalorielimit = profile.value.weekcalorielimit
      editProfile.weight = profile.value.weight
      editSelectedFoodTypes.value = [...selectedFoodTypes.value]
      editSelectedExerciseNames.value = [...selectedExerciseNames.value]
      editSelectedRestaurantIds.value = [...selectedRestaurantIds.value]
      isEditing.value = true
    }

    // 儲存編輯
    const saveEdit = async () => {
      isLoading.value = true
      errorMsg.value = ''
      try {
        const token = localStorage.getItem('token')
        const userId = Number(localStorage.getItem('userId'))
        if (!userId) {
          errorMsg.value = '找不到使用者 ID，請重新登入'
          isLoading.value = false
          return
        }
        // 1. 儲存基本資料
        const payload = {
          name: editProfile.name,
          email: editProfile.email,
          budget: editProfile.budget,
          weekcalorielimit: editProfile.weekcalorielimit,
          weight: editProfile.weight
        }
        await axios.put('/api/auth/profile', payload, {
          headers: { Authorization: `Bearer ${token}` }
        })
        // 2. 儲存三種偏好（PUT）
        await axios.put('/api/user/food-preferences', { user_id: userId, food_types: editSelectedFoodTypes.value })
        await axios.put('/api/user/exercise-preferences', { user_id: userId, exercise_names: editSelectedExerciseNames.value })
        await axios.put('/api/user/restaurant-preferences', { user_id: userId, restaurant_ids: editSelectedRestaurantIds.value })
        // 更新顯示資料
        profile.value.name = editProfile.name
        profile.value.email = editProfile.email
        profile.value.budget = editProfile.budget
        profile.value.weekcalorielimit = editProfile.weekcalorielimit
        profile.value.weight = editProfile.weight
        selectedFoodTypes.value = [...editSelectedFoodTypes.value]
        selectedExerciseNames.value = [...editSelectedExerciseNames.value]
        selectedRestaurantIds.value = [...editSelectedRestaurantIds.value]
        isEditing.value = false
        dialogMsg.value = '資料已儲存！'
        dialogVisible.value = true
      } catch (err) {
        errorMsg.value = err.response?.data?.error || '儲存失敗'
        dialogMsg.value = errorMsg.value
        dialogVisible.value = true
      } finally {
        isLoading.value = false
      }
    }

    // 取消編輯
    const cancelEdit = () => {
      isEditing.value = false
      errorMsg.value = ''
    }

    // 餐廳名稱查找
    const getRestaurantName = (id) => {
      const r = restaurants.value.find(r => r.id === id)
      return r ? r.name : id
    }

    onMounted(async () => {
      await fetchOptions()
      await fetchProfile()
      const userId = Number(localStorage.getItem('userId'))
      if (userId) await fetchUserPreferences(userId)
    })
    
    return {
      profile,
      isLoading,
      isEditing,
      errorMsg,
      foodTypes,
      exerciseItems,
      restaurants,
      selectedFoodTypes,
      selectedExerciseNames,
      selectedRestaurantIds,
      editProfile,
      editSelectedFoodTypes,
      editSelectedExerciseNames,
      editSelectedRestaurantIds,
      startEdit,
      saveEdit,
      cancelEdit,
      dialogVisible,
      dialogMsg,
      getRestaurantName
    }
  }
}
</script>

<style scoped>
.basic-info-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 40px 0;
  background: #fff7e6;
}
.profile-card {
  width: 100%;
  max-width: 650px;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(240,140,0,0.10);
  padding: 32px 24px 24px 24px;
  border: 2px solid #f08c0022;
  background: #fff;
}
.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}
.edit-btn, .save-btn {
  background: #f08c00 !important;
  border-color: #f08c00 !important;
  color: #fff !important;
}
.preference-card, .preference-view {
  margin: 18px 0 0 0;
  padding: 18px 16px;
  border-radius: 8px;
  background: #f9fafb;
  box-shadow: 0 2px 8px rgba(240,140,0,0.04);
  border: 1.5px solid #f08c0033;
}
.preference-header {
  margin-bottom: 10px;
  font-weight: 600;
  color: #f08c00;
  display: flex;
  align-items: center;
}
.pref-block {
  margin-bottom: 12px;
  display: flex;
  align-items: center;
}
.pref-title {
  font-weight: 600;
  color: #f08c00;
  margin-right: 8px;
  display: flex;
  align-items: center;
}
.pref-tag {
  margin-right: 6px;
  margin-bottom: 4px;
  font-size: 15px;
  border-radius: 16px;
  padding: 0 10px;
  background: #fff7e6;
  color: #f08c00;
  border-color: #f08c00;
}
.pref-empty {
  color: #bbb;
  font-style: italic;
}
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}
@media (max-width: 700px) {
  .profile-card { padding: 16px 4px; }
}
</style> 