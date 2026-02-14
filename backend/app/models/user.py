from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, Sequence
from app.database import Base


class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    real_name = Column(String)
    phone = Column(String)
    qq = Column(String)
    wechat = Column(String)
    address = Column(String)
    bio = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    @classmethod
    def get_by_id(cls, db: Session, user_id: int) -> Optional['User']:
        """根据ID获取用户"""
        return db.query(cls).filter(cls.id == user_id).first()
    
    @classmethod
    def get_by_username(cls, db: Session, username: str) -> Optional['User']:
        """根据用户名获取用户"""
        return db.query(cls).filter(cls.username == username).first()
    
    @classmethod
    def get_by_email(cls, db: Session, email: str) -> Optional['User']:
        """根据邮箱获取用户"""
        return db.query(cls).filter(cls.email == email).first()
    
    @classmethod
    def get_by_real_name(cls, db: Session, real_name: str) -> Optional['User']:
        """根据真实姓名获取用户"""
        return db.query(cls).filter(cls.real_name == real_name).first()
    
    @classmethod
    def get_all(cls, db: Session, limit: int = 100, offset: int = 0) -> Sequence['User']:
        """获取所有用户"""
        return db.query(cls).limit(limit).offset(offset).all()
    
    @classmethod
    def create(cls, db: Session, username: str, password_hash: str, email: Optional[str] = None, real_name: Optional[str] = None, phone: Optional[str] = None, qq: Optional[str] = None, wechat: Optional[str] = None, address: Optional[str] = None, bio: Optional[str] = None) -> 'User':
        """创建新用户"""
        db_user = cls(
            username=username,
            password_hash=password_hash,
            email=email,
            real_name=real_name,
            phone=phone,
            qq=qq,
            wechat=wechat,
            address=address,
            bio=bio
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def update(self, db: Session, **kwargs) -> 'User':
        """更新用户信息"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        # 更新updated_at
        self.updated_at = datetime.now()
        
        db.commit()
        db.refresh(self)
        return self
    
    def delete(self, db: Session) -> None:
        """删除用户"""
        db.delete(self)
        db.commit()
