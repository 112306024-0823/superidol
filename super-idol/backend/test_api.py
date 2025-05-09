"""
整合測試 - 直接使用真實資料庫進行測試
"""
from app import create_app
import unittest
import time
import random
import string
import pytest

@pytest.fixture
def client():
    """創建測試用的 Flask client"""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c

def generate_random_email():
    """生成隨機的電子郵件地址以避免衝突"""
    timestamp = int(time.time())
    random_str = ''.join(random.choices(string.ascii_lowercase, k=5))
    return f"test_{timestamp}_{random_str}@example.com"

def test_signup(client):
    """測試註冊功能"""
    # 使用隨機生成的電子郵件
    email = generate_random_email()
    name = f"TestUser_{random.randint(1000, 9999)}"
    
    # 發送註冊請求
    response = client.post(
        '/api/auth/signup',
        json={
            'name': name,
            'email': email,
            'password': 'password123'
        }
    )
    
    # 驗證回應
    assert response.status_code == 201, f"註冊失敗，狀態碼: {response.status_code}，回應: {response.get_json()}"
    data = response.get_json()
    assert 'access_token' in data, "回應中缺少 access_token"
    assert 'user' in data, "回應中缺少 user 資訊"
    assert data['user']['email'] == email, "回傳的電子郵件與發送的不一致"

def test_login(client):
    """測試登入功能"""
    # 先註冊一個用戶
    email = generate_random_email()
    name = f"LoginTest_{random.randint(1000, 9999)}"
    
    # 註冊用戶
    signup_response = client.post(
        '/api/auth/signup',
        json={
            'name': name,
            'email': email,
            'password': 'password123'
        }
    )
    assert signup_response.status_code == 201, "無法建立測試用戶"
    
    # 使用該用戶進行登入測試
    response = client.post(
        '/api/auth/login',
        json={
            'email': email,
            'password': 'password123'
        }
    )
    
    # 驗證回應
    assert response.status_code == 200, f"登入失敗，狀態碼: {response.status_code}，回應: {response.get_json()}"
    data = response.get_json()
    assert 'access_token' in data, "回應中缺少 access_token"
    assert data['user']['email'] == email, "回傳的電子郵件與發送的不一致"

def test_login_with_wrong_password(client):
    """測試使用錯誤密碼登入"""
    # 先註冊一個用戶
    email = generate_random_email()
    name = f"WrongPassTest_{random.randint(1000, 9999)}"
    
    # 註冊用戶
    signup_response = client.post(
        '/api/auth/signup',
        json={
            'name': name,
            'email': email,
            'password': 'password123'
        }
    )
    assert signup_response.status_code == 201, "無法建立測試用戶"
    
    # 使用錯誤密碼進行登入
    response = client.post(
        '/api/auth/login',
        json={
            'email': email,
            'password': 'wrong_password'
        }
    )
    
    # 驗證回應是否為401 Unauthorized
    assert response.status_code == 401, "使用錯誤密碼應返回401狀態碼"
    data = response.get_json()
    assert 'error' in data, "回應中應包含錯誤訊息"

if __name__ == '__main__':
    # 可以直接運行此文件進行測試
    pytest.main(['-xvs', __file__])
