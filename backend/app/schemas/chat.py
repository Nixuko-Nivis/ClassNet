from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict, Any


class MessageBase(BaseModel):
    """消息基础模型"""
    room_id: str = Field(..., description="房间ID")
    content: str = Field(..., description="消息内容")


class MessageCreate(MessageBase):
    """消息创建模型"""
    pass


class MessageInDB(MessageBase):
    """数据库中的消息模型"""
    id: int
    sender_id: int
    timestamp: datetime
    
    class Config:
        from_attributes = True


class Message(MessageBase):
    """消息响应模型"""
    id: int
    sender_id: int
    timestamp: datetime
    sender: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True


class MessageList(BaseModel):
    """消息列表响应模型"""
    messages: list[Message]
    total: int


class SendMessageRequest(BaseModel):
    """发送消息请求模型"""
    room_id: str = Field(..., description="房间ID")
    content: str = Field(..., description="消息内容")


class SendMessageResponse(BaseModel):
    """发送消息响应模型"""
    code: int
    message: str
    data: dict


class MessageListResponse(BaseModel):
    """消息列表响应模型"""
    code: int
    message: str
    data: list
