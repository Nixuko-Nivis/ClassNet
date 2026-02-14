from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Session, relationship
from datetime import datetime
from typing import Optional, List, Sequence
from app.database import Base


class Message(Base):
    """聊天消息模型"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    room_id = Column(String, nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # 关系
    sender = relationship("User", backref="messages")
    
    @classmethod
    def get_by_id(cls, db: Session, message_id: int) -> Optional['Message']:
        """根据ID获取消息"""
        return db.query(cls).filter(cls.id == message_id).first()
    
    @classmethod
    def get_by_room_id(cls, db: Session, room_id: str, limit: int = 50, offset: int = 0) -> Sequence['Message']:
        """根据房间ID获取消息"""
        return db.query(cls).filter(cls.room_id == room_id)\
            .order_by(cls.timestamp.desc())\
            .limit(limit)\
            .offset(offset)\
            .all()
    
    @classmethod
    def get_by_sender_id(cls, db: Session, sender_id: int, limit: int = 50, offset: int = 0) -> Sequence['Message']:
        """根据发送者ID获取消息"""
        return db.query(cls).filter(cls.sender_id == sender_id)\
            .order_by(cls.timestamp.desc())\
            .limit(limit)\
            .offset(offset)\
            .all()
    
    @classmethod
    def create(cls, db: Session, room_id: str, sender_id: int, content: str) -> 'Message':
        """创建新消息"""
        db_message = cls(
            room_id=room_id,
            sender_id=sender_id,
            content=content
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message
    
    def update(self, db: Session, **kwargs) -> 'Message':
        """更新消息信息"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        db.commit()
        db.refresh(self)
        return self
    
    def delete(self, db: Session) -> None:
        """删除消息"""
        db.delete(self)
        db.commit()
