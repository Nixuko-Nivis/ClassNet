from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.websockets import WebSocket, WebSocketDisconnect
from app.schemas import chat as chat_schemas
from app.services import chat_service
from app.api.auth import oauth2_scheme
from app.utils import security

router = APIRouter()


@router.get("/messages", response_model=chat_schemas.MessageListResponse)
def get_messages(
    room_id: str = Query(..., description="聊天室ID"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    token: str = Depends(oauth2_scheme)
):
    """获取聊天消息"""
    try:
        # 验证令牌
        security.verify_token(token)
        
        messages = chat_service.get_messages(
            room_id=room_id,
            limit=limit,
            offset=offset
        )
        return {
            "code": 200,
            "message": "获取消息成功",
            "data": messages
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌"
        )


@router.post("/send", response_model=chat_schemas.SendMessageResponse)
def send_message(
    message_data: chat_schemas.SendMessageRequest,
    token: str = Depends(oauth2_scheme)
):
    """发送消息"""
    try:
        # 验证令牌
        user_id = security.verify_token(token)
        
        # 确保user_id是整数
        try:
            user_id_int = int(user_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="无效的用户ID"
            )
        
        message_id = chat_service.send_message(
            room_id=message_data.room_id,
            sender_id=user_id_int,
            content=message_data.content
        )
        return {
            "code": 200,
            "message": "发送成功",
            "data": {
                "message_id": message_id
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌"
        )


@router.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    """WebSocket聊天端点"""
    await websocket.accept()
    # 连接到房间
    await chat_service.manager.connect(websocket, room_id)
    try:
        while True:
            # 接收消息
            data = await websocket.receive_json()
            # 处理消息
            await chat_service.handle_websocket(
                websocket=websocket,
                room_id=room_id,
                data=data
            )
    except WebSocketDisconnect:
        # 处理断开连接
        chat_service.manager.disconnect(websocket, room_id)
