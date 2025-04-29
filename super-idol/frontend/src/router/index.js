/* 
    檔案：index.js
    用途：路由配置
    功能：
    - 定義應用程式的路由
    - 處理路由導航
*/
import { createRouter, createWebHistory } from 'vue-router';

const routes = [
    {
        path: '/',
        name: 'home',
        component: () => import('@/pages/home/index.html')
    },
    {
        path: '/login',
        name: 'login',
        component: () => import('@/pages/login/index.html')
    },
    {
        path: '/register',
        name: 'register',
        component: () => import('@/pages/register/index.html')
    },
    {
        path: '/user_profile',
        name: 'user_profile',
        component: () => import('@/pages/user_profile/index.html'),
        meta: { requiresAuth: true }
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

// 路由守衛
router.beforeEach((to, from, next) => {
    const isAuthenticated = localStorage.getItem('token');
    
    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/login');
    } else {
        next();
    }
});

export default router; 