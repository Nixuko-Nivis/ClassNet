import requests

# 测试注册新用户
def test_register():
    url = "http://localhost:8000/api/auth/register"
    data = {
        "username": "testuser1",
        "password": "password123",
        "email": "testuser1@example.com"
    }
    response = requests.post(url, json=data)
    print("Register response:", response.status_code, response.json())
    return response.status_code == 200

# 测试登录新用户
def test_login():
    url = "http://localhost:8000/api/auth/login"
    data = {
        "username": "testuser1",
        "password": "password123"
    }
    response = requests.post(url, data=data)
    print("Login response:", response.status_code, response.json())
    if response.status_code == 200:
        return response.json().get("data", {}).get("access_token")
    return None

if __name__ == "__main__":
    print("Testing registration...")
    if test_register():
        print("Registration successful, testing login...")
        token = test_login()
        if token:
            print(f"Login successful! Token: {token[:20]}...")
        else:
            print("Login failed")
    else:
        print("Registration failed")
