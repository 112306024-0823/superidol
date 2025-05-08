<template>
  <div id="app">
    <header v-if="isAuthenticated && !isAuthPage">
      <Header />
    </header>
    <div class="main-container" :class="{ 'with-sidebar': isAuthenticated && !isAuthPage }">
      <aside v-if="isAuthenticated && !isAuthPage" class="sidebar">
        <Sidebar />
      </aside>
      <main class="content">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from './store/auth'
import Header from './components/layout/Header.vue'
import Sidebar from './components/layout/Sidebar.vue'

export default {
  name: 'App',
  components: {
    Header,
    Sidebar
  },
  setup() {
    const route = useRoute()
    const authStore = useAuthStore()

    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const isAuthPage = computed(() => {
      return route.path === '/login' || route.path === '/register'
    })

    return {
      isAuthenticated,
      isAuthPage
    }
  }
}
</script>

<style>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-container {
  display: flex;
  flex: 1;
}

.with-sidebar {
  padding-left: 240px;
}

.sidebar {
  position: fixed;
  width: 240px;
  left: 0;
  top: 64px;
  bottom: 0;
  background-color: var(--card-bg);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.content {
  flex: 1;
  padding-top: 64px;
}

@media (max-width: 768px) {
  .with-sidebar {
    padding-left: 0;
  }
  
  .sidebar {
    transform: translateX(-100%);
    transition: transform 0.3s ease;
  }
  
  .sidebar.open {
    transform: translateX(0);
  }
}
</style> 