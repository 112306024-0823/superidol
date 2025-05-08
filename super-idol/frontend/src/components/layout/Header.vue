<template>
  <div class="app-header">
    <div class="container header-container">
      <div class="logo-container">
        <router-link to="/dashboard" class="logo">
          <span class="logo-text">速per Idol</span>
        </router-link>
      </div>
      
      <div class="nav-desktop">
        <nav class="main-nav">
          <router-link to="/dashboard" class="nav-link">儀表板</router-link>
          <router-link to="/food/record" class="nav-link">食物記錄</router-link>
          <router-link to="/food/search" class="nav-link">食物搜尋</router-link>
          <router-link to="/exercise/record" class="nav-link">運動記錄</router-link>
          <router-link to="/reports/weekly" class="nav-link">週報告</router-link>
        </nav>
        
        <div class="user-menu">
          <button class="user-toggle" @click="isMenuOpen = !isMenuOpen">
            <span class="user-name">{{ userName }}</span>
            <i class="icon-chevron-down"></i>
          </button>
          
          <div v-if="isMenuOpen" class="dropdown-menu">
            <router-link to="/profile/basic-info" class="dropdown-item">個人資料</router-link>
            <router-link to="/profile/favorites" class="dropdown-item">我的最愛</router-link>
            <button class="dropdown-item" @click="logout">登出</button>
          </div>
        </div>
      </div>
      
      <button class="mobile-toggle" @click="isMobileMenuOpen = !isMobileMenuOpen">
        <i class="icon-menu"></i>
      </button>
    </div>
    
    <div v-if="isMobileMenuOpen" class="mobile-menu">
      <nav class="mobile-nav">
        <router-link to="/dashboard" class="nav-link">儀表板</router-link>
        <router-link to="/food/record" class="nav-link">食物記錄</router-link>
        <router-link to="/food/search" class="nav-link">食物搜尋</router-link>
        <router-link to="/exercise/record" class="nav-link">運動記錄</router-link>
        <router-link to="/reports/weekly" class="nav-link">週報告</router-link>
        <router-link to="/profile/basic-info" class="nav-link">個人資料</router-link>
        <router-link to="/profile/favorites" class="nav-link">我的最愛</router-link>
        <button class="nav-link logout-button" @click="logout">登出</button>
      </nav>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth'

export default {
  name: 'AppHeader',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    const isMenuOpen = ref(false)
    const isMobileMenuOpen = ref(false)
    
    const userName = computed(() => {
      return authStore.user?.name || 'User'
    })
    
    const logout = async () => {
      await authStore.logout()
      router.push('/login')
    }
    
    return {
      isMenuOpen,
      isMobileMenuOpen,
      userName,
      logout
    }
  }
}
</script>

<style scoped>
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  background-color: var(--primary-color);
  color: white;
  z-index: 1000;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
}

.logo-container {
  display: flex;
  align-items: center;
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: white;
}

.logo-text {
  font-size: 24px;
  font-weight: bold;
}

.nav-desktop {
  display: flex;
  align-items: center;
}

.main-nav {
  display: flex;
  margin-right: 24px;
}

.nav-link {
  padding: 8px 16px;
  color: white;
  text-decoration: none;
  opacity: 0.8;
  transition: opacity 0.3s;
}

.nav-link:hover,
.nav-link.router-link-active {
  opacity: 1;
}

.user-menu {
  position: relative;
}

.user-toggle {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  padding: 8px;
}

.user-name {
  margin-right: 8px;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  width: 180px;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  z-index: 1000;
}

.dropdown-item {
  display: block;
  padding: 12px 16px;
  color: var(--text-color);
  text-decoration: none;
  width: 100%;
  text-align: left;
  border: none;
  background: none;
  cursor: pointer;
  font-size: 16px;
}

.dropdown-item:hover {
  background-color: #f5f5f5;
}

.mobile-toggle {
  display: none;
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
}

.mobile-menu {
  display: none;
  position: fixed;
  top: 64px;
  left: 0;
  right: 0;
  background-color: var(--primary-color);
  padding: 16px;
  z-index: 999;
}

.mobile-nav {
  display: flex;
  flex-direction: column;
}

.mobile-nav .nav-link {
  padding: 12px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.logout-button {
  background: none;
  border: none;
  color: white;
  text-align: left;
  width: 100%;
  font-size: 16px;
  padding: 12px 0;
  cursor: pointer;
}

@media (max-width: 768px) {
  .nav-desktop {
    display: none;
  }
  
  .mobile-toggle {
    display: block;
  }
  
  .mobile-menu {
    display: block;
  }
}
</style> 