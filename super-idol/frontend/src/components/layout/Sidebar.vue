<template>
  <div class="sidebar-container">
    <nav class="sidebar-nav">
      <div class="nav-section">
        <h3 class="nav-section-title">主要功能</h3>
        <router-link to="/dashboard" class="nav-item">
          <i class="icon-dashboard"></i>
          <span>儀表板</span>
        </router-link>
        <router-link to="/food/record" class="nav-item">
          <i class="icon-food"></i>
          <span>食物記錄</span>
        </router-link>
        <router-link to="/food/search" class="nav-item">
          <i class="icon-search"></i>
          <span>食物搜尋</span>
        </router-link>
        <router-link to="/exercise/record" class="nav-item">
          <i class="icon-dumbbell"></i>
          <span>運動記錄</span>
        </router-link>
        <router-link to="/reports/weekly" class="nav-item">
          <i class="icon-chart"></i>
          <span>週報告</span>
        </router-link>
      </div>
      
      <div class="nav-section">
        <h3 class="nav-section-title">個人</h3>
        <router-link to="/profile/basic-info" class="nav-item">
          <i class="icon-user"></i>
          <span>個人資料</span>
        </router-link>
        <router-link to="/profile/favorites" class="nav-item">
          <i class="icon-heart"></i>
          <span>我的最愛</span>
        </router-link>
      </div>
    </nav>
    
    <div class="sidebar-footer">
      <button class="logout-button" @click="logout">
        <i class="icon-logout"></i>
        <span>登出</span>
      </button>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth'

export default {
  name: 'AppSidebar',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    const logout = async () => {
      await authStore.logout()
      router.push('/login')
    }
    
    return {
      logout
    }
  }
}
</script>

<style scoped>
.sidebar-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 16px;
}

.sidebar-nav {
  flex: 1;
}

.nav-section {
  margin-bottom: 24px;
}

.nav-section-title {
  font-size: 14px;
  color: #777;
  margin-bottom: 12px;
  padding-left: 12px;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 12px;
  color: var(--text-color);
  text-decoration: none;
  border-radius: 4px;
  transition: background-color 0.2s;
  margin-bottom: 4px;
}

.nav-item:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.nav-item.router-link-active {
  background-color: rgba(var(--primary-color-rgb), 0.1);
  color: var(--primary-color);
  font-weight: 500;
}

.nav-item i {
  margin-right: 12px;
  font-size: 20px;
  /* 使用偽元素作為圖標，待補充實際圖標 */
  width: 20px;
  height: 20px;
  display: inline-block;
}

.sidebar-footer {
  padding: 16px 0;
  border-top: 1px solid #eee;
}

.logout-button {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 12px;
  background: none;
  border: none;
  border-radius: 4px;
  color: var(--text-color);
  cursor: pointer;
  font-size: 16px;
  text-align: left;
  transition: background-color 0.2s;
}

.logout-button:hover {
  background-color: rgba(0, 0, 0, 0.05);
}

.logout-button i {
  margin-right: 12px;
  font-size: 20px;
  /* 使用偽元素作為圖標，待補充實際圖標 */
  width: 20px;
  height: 20px;
  display: inline-block;
}
</style> 