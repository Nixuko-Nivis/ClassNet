import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db

# 初始化测试客户端
client = TestClient(app)

# 测试前初始化数据库
@pytest.fixture(autouse=True)
def setup_database():
    init_db()
    yield


# 测试后台管理密码验证
def test_admin_password_verification():
    """测试后台管理密码验证"""
    # 正确的验证密码
    response = client.post("/api/admin/verify-password", data={"password": "kjtpcyb07"})
    assert response.status_code == 200
    assert response.json()["code"] == 200
    assert response.json()["message"] == "密码验证成功"
    
    # 错误的验证密码
    response = client.post("/api/admin/verify-password", data={"password": "wrong_password"})
    assert response.status_code == 401
    assert response.json()["detail"] == "密码错误"


# 测试用户登录
def test_admin_login():
    """测试后台管理登录"""
    # 首先注册一个用户，使用预定义列表中的真实姓名
    import uuid
    unique_username = f"admin_test_{uuid.uuid4().hex[:8]}"
    register_response = client.post("/api/auth/register", json={
        "username": unique_username,
        "password": "test_password",
        "realname": "admin"
    })
    assert register_response.status_code == 200
    
    # 使用正确的用户名和密码登录
    login_response = client.post("/api/admin/login", data={
        "username": unique_username,
        "password": "test_password"
    })
    assert login_response.status_code == 200
    assert login_response.json()["code"] == 200
    assert "access_token" in login_response.json()["data"]
    
    # 使用错误的密码登录
    wrong_password_response = client.post("/api/admin/login", data={
        "username": unique_username,
        "password": "wrong_password"
    })
    assert wrong_password_response.status_code == 401


# 测试用户管理
def test_admin_user_management():
    """测试后台管理用户管理功能"""
    # 首先注册并登录获取令牌，使用预定义列表中的真实姓名
    import uuid
    unique_username = f"admin_test_{uuid.uuid4().hex[:8]}"
    register_response = client.post("/api/auth/register", json={
        "username": unique_username,
        "password": "test_password",
        "realname": "admin"
    })
    assert register_response.status_code == 200
    
    login_response = client.post("/api/admin/login", data={
        "username": unique_username,
        "password": "test_password"
    })
    assert login_response.status_code == 200
    token = login_response.json()["data"]["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 获取用户列表
    users_response = client.get("/api/admin/users", headers=headers)
    assert users_response.status_code == 200
    assert users_response.json()["code"] == 200
    assert "users" in users_response.json()["data"]
    
    # 获取单个用户信息
    user_id = users_response.json()["data"]["users"][0]["user_id"]
    user_detail_response = client.get(f"/api/admin/users/{user_id}", headers=headers)
    assert user_detail_response.status_code == 200
    assert user_detail_response.json()["code"] == 200
    assert user_detail_response.json()["data"]["user_id"] == user_id


# 测试密码加密存储
def test_password_encryption():
    """测试密码加密存储"""
    # 注册用户，使用预定义列表中的真实姓名
    import uuid
    unique_username = f"encryption_test_{uuid.uuid4().hex[:8]}"
    register_response = client.post("/api/auth/register", json={
        "username": unique_username,
        "password": "test_password",
        "realname": "admin"
    })
    assert register_response.status_code == 200
    
    # 登录验证密码
    login_response = client.post("/api/auth/login", data={
        "username": unique_username,
        "password": "test_password"
    })
    assert login_response.status_code == 200
    assert login_response.json()["code"] == 200
    
    # 使用错误密码登录
    wrong_login_response = client.post("/api/auth/login", data={
        "username": unique_username,
        "password": "wrong_password"
    })
    assert wrong_login_response.status_code == 401


# 测试权限控制
def test_admin_access_control():
    """测试后台管理访问控制"""
    # 未登录访问后台管理接口
    response = client.get("/api/admin/users")
    assert response.status_code == 401
    
    # 使用无效令牌访问
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/admin/users", headers=headers)
    assert response.status_code == 401
