from typing import List, Dict, Any
from fastapi.websockets import WebSocket
from app.models.chat import Message
from app.database import get_db

# WebSocket连接管理器
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, room_id: str):
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, room_id: str):
        if room_id in self.active_connections:
            self.active_connections[room_id].remove(websocket)
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]
    
    async def broadcast(self, message: Dict[str, Any], room_id: str):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    self.disconnect(connection, room_id)

manager = ConnectionManager()


def get_messages(room_id: str, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """获取聊天消息"""
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        messages = Message.get_by_room_id(db, room_id, limit=limit, offset=offset)
        result = []
        for message in messages:
            try:
                sender_name = message.sender.name if message.sender else "未知用户"
            except Exception:
                sender_name = "未知用户"
            result.append({
                "id": message.id,
                "room_id": message.room_id,
                "sender_id": message.sender_id,
                "sender_name": sender_name,
                "content": message.content,
                "timestamp": message.timestamp.isoformat()
            })
        return result
    finally:
        db.close()


def send_message(room_id: str, sender_id: int, content: str) -> str:
    """发送消息"""
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        message = Message.create(
            db=db,
            room_id=room_id,
            sender_id=sender_id,
            content=content
        )
        
        if not message:
            raise ValueError("消息创建失败")
        
        # 获取消息ID并转换为字符串
        message_id = message.id
        return str(message_id)
    finally:
        db.close()


async def handle_websocket(websocket: WebSocket, room_id: str, data: Dict[str, Any]):
    """处理WebSocket连接"""
    try:
        # 处理消息
        sender_id = data.get("sender_id", "")
        content = data.get("content", "")
        
        if not sender_id or not content:
            return
        
        # 确保sender_id是整数
        try:
            sender_id_int = int(sender_id)
        except ValueError:
            await websocket.send_json({"error": "无效的发送者ID"})
            return
        
        message_id = send_message(
            room_id=room_id,
            sender_id=sender_id_int,
            content=content
        )
        
        # 广播消息
        await manager.broadcast(
            {
                "message_id": message_id,
                "room_id": room_id,
                "sender_id": sender_id,
                "content": content,
                "timestamp": data.get("timestamp", "")
            },
            room_id
        )
    except Exception as e:
        # 发送错误消息给客户端
        try:
            await websocket.send_json({"error": str(e)})
        except:
            pass
