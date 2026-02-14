import requests
import json

# 测试登录
def test_login():
    url = "http://localhost:8000/api/auth/login"
    data = {
        "username": "testuser",
        "password": "password123"
    }
    # 使用表单数据而不是JSON
    response = requests.post(url, data=data)
    print("Login response:", response.status_code, response.json())
    if response.status_code == 200:
        return response.json().get("data", {}).get("access_token")
    return None

# 测试获取消息
def test_get_messages(token):
    url = "http://localhost:8000/api/chat/messages"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    params = {
        "room_id": "test_room",
        "limit": 50,
        "offset": 0
    }
    response = requests.get(url, headers=headers, params=params)
    print("Get messages response:", response.status_code, response.json())

# 测试发送消息
def test_send_message(token):
    url = "http://localhost:8000/api/chat/send"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    data = {
        "room_id": "test_room",
        "content": "Hello, this is a test message!"
    }
    response = requests.post(url, headers=headers, json=data)
    print("Send message response:", response.status_code, response.json())

if __name__ == "__main__":
    print("Testing chat module...")
    token = test_login()
    if token:
        print(f"Got token: {token[:20]}...")
        test_send_message(token)
        test_get_messages(token)
    else:
        print("Login failed, cannot test chat module")
