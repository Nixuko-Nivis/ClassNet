import requests

# 使用从登录获取的令牌
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzIiwiZXhwIjoxNzcwNTUxMDM4fQ.d2aMaoPo0cotWr_4xivO1OwPPe0ucl8JsShz9EJ86LQ"

# 测试获取消息
def test_get_messages():
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
def test_send_message():
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
    print("Sending test message...")
    test_send_message()
    print("Getting messages...")
    test_get_messages()
