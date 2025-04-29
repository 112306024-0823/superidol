<!-- 
    檔案：Navigation.vue
    用途：導航選單組件
    功能：
    - 提供網站導航功能
    - 顯示用戶狀態
-->
<template>
    <nav class="navigation">
        <div class="logo">
            <router-link to="/">Super Idol</router-link>
        </div>
        <div class="nav-links">
            <router-link to="/" class="nav-link">首頁</router-link>
            <router-link to="/food" class="nav-link">食物</router-link>
            <router-link to="/report" class="nav-link">報告</router-link>
            <router-link to="/user_profile" class="nav-link">個人資料</router-link>
        </div>
        <div class="user-actions">
            <template v-if="isAuthenticated">
                <span class="username">{{ username }}</span>
                <button @click="logout" class="btn-logout">登出</button>
            </template>
            <template v-else>
                <router-link to="/login" class="btn-login">登入</router-link>
                <router-link to="/register" class="btn-register">註冊</router-link>
            </template>
        </div>
    </nav>
</template>

<script>
export default {
    name: 'Navigation',
    data() {
        return {
            isAuthenticated: false,
            username: ''
        };
    },
    methods: {
        checkAuth() {
            const token = localStorage.getItem('token');
            const user = JSON.parse(localStorage.getItem('user'));
            
            this.isAuthenticated = !!token;
            this.username = user?.username || '';
        },
        logout() {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            this.$router.push('/login');
        }
    },
    mounted() {
        this.checkAuth();
    }
};
</script>

<style scoped>
.navigation {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 60px;
    background-color: white;
    box-shadow: var(--shadow-sm);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 var(--spacing-lg);
    z-index: 1000;
}

.logo a {
    font-size: 1.5rem;
    font-weight: bold;
    color: var(--primary-color);
    text-decoration: none;
}

.nav-links {
    display: flex;
    gap: var(--spacing-md);
}

.nav-link {
    color: var(--text-color);
    text-decoration: none;
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--border-radius);
    transition: background-color var(--transition-fast);
}

.nav-link:hover {
    background-color: var(--bg-light);
}

.nav-link.router-link-active {
    color: var(--primary-color);
    font-weight: 500;
}

.user-actions {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
}

.username {
    color: var(--text-color);
    font-weight: 500;
}

.btn-login,
.btn-register,
.btn-logout {
    padding: var(--spacing-sm) var(--spacing-md);
    border-radius: var(--border-radius);
    cursor: pointer;
    transition: background-color var(--transition-fast);
}

.btn-login {
    background-color: var(--primary-color);
    color: white;
}

.btn-register {
    background-color: var(--secondary-color);
    color: white;
}

.btn-logout {
    background-color: var(--danger-color);
    color: white;
}

.btn-login:hover {
    background-color: var(--primary-dark);
}

.btn-register:hover {
    background-color: var(--secondary-dark);
}

.btn-logout:hover {
    background-color: var(--danger-dark);
}
</style> 