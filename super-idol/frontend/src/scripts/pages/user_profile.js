/* 
    檔案：user_profile.js
    用途：用戶個人資料頁面的腳本
    功能：
    - 載入用戶資料
    - 處理用戶資料編輯
    - 處理密碼修改
*/
import { userAPI } from '@/services/api';

// DOM 元素
const elements = {
    avatar: document.querySelector('.avatar-img'),
    username: document.querySelector('.username'),
    email: document.querySelector('.email'),
    name: document.querySelector('.name'),
    gender: document.querySelector('.gender'),
    age: document.querySelector('.age'),
    height: document.querySelector('.height'),
    weight: document.querySelector('.weight'),
    goal: document.querySelector('.goal'),
    calorieGoal: document.querySelector('.calorie-goal'),
    proteinGoal: document.querySelector('.protein-goal'),
    carbsGoal: document.querySelector('.carbs-goal'),
    fatGoal: document.querySelector('.fat-goal'),
    btnEdit: document.querySelector('.btn-edit'),
    btnChangePassword: document.querySelector('.btn-change-password')
};

// 載入用戶資料
async function loadUserProfile() {
    try {
        const userData = await userAPI.getProfile();
        updateProfileUI(userData);
    } catch (error) {
        console.error('載入用戶資料失敗:', error);
        showError('載入用戶資料失敗，請稍後再試');
    }
}

// 更新 UI
function updateProfileUI(data) {
    elements.avatar.src = data.avatar || '/images/default-avatar.png';
    elements.username.textContent = data.username;
    elements.email.textContent = data.email;
    elements.name.textContent = data.name;
    elements.gender.textContent = data.gender;
    elements.age.textContent = `${data.age} 歲`;
    elements.height.textContent = `${data.height} cm`;
    elements.weight.textContent = `${data.weight} kg`;
    elements.goal.textContent = data.goal;
    elements.calorieGoal.textContent = `${data.calorieGoal} kcal`;
    elements.proteinGoal.textContent = `${data.proteinGoal} g`;
    elements.carbsGoal.textContent = `${data.carbsGoal} g`;
    elements.fatGoal.textContent = `${data.fatGoal} g`;
}

// 編輯資料
elements.btnEdit.addEventListener('click', () => {
    // TODO: 實現編輯資料功能
    console.log('編輯資料');
});

// 修改密碼
elements.btnChangePassword.addEventListener('click', () => {
    // TODO: 實現修改密碼功能
    console.log('修改密碼');
});

// 顯示錯誤訊息
function showError(message) {
    // TODO: 實現錯誤提示功能
    console.error(message);
}

// 初始化
document.addEventListener('DOMContentLoaded', loadUserProfile); 