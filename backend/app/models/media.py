from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List, Sequence
from app.database import Base


class MediaFile(Base):
    """媒体文件模型"""
    __tablename__ = "media_files"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    file_name = Column(String, nullable=False, index=True)
    file_path = Column(String, unique=True, nullable=False, index=True)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String, nullable=False, index=True)
    extension = Column(String, nullable=False, index=True)
    create_time = Column(DateTime(timezone=True), server_default=func.now())
    modify_time = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    @classmethod
    def get_by_id(cls, db: Session, file_id: int) -> Optional['MediaFile']:
        """根据ID获取媒体文件"""
        return db.query(cls).filter(cls.id == file_id).first()
    
    @classmethod
    def get_by_path(cls, db: Session, file_path: str) -> Optional['MediaFile']:
        """根据路径获取媒体文件"""
        return db.query(cls).filter(cls.file_path == file_path).first()
    
    @classmethod
    def get_by_type(cls, db: Session, file_type: str, limit: int = 100, offset: int = 0) -> Sequence['MediaFile']:
        """根据类型获取媒体文件"""
        return db.query(cls).filter(cls.file_type == file_type)\
            .limit(limit)\
            .offset(offset)\
            .all()
    
    @classmethod
    def get_by_extension(cls, db: Session, extension: str, limit: int = 100, offset: int = 0) -> Sequence['MediaFile']:
        """根据扩展名获取媒体文件"""
        return db.query(cls).filter(cls.extension == extension)\
            .limit(limit)\
            .offset(offset)\
            .all()
    
    @classmethod
    def get_all(cls, db: Session, limit: int = 100, offset: int = 0) -> Sequence['MediaFile']:
        """获取所有媒体文件"""
        return db.query(cls)\
            .order_by(cls.create_time.desc())\
            .limit(limit)\
            .offset(offset)\
            .all()
    
    @classmethod
    def create(cls, db: Session, file_name: str, file_path: str, file_size: int, file_type: str, extension: str) -> 'MediaFile':
        """创建新媒体文件记录"""
        db_media = cls(
            file_name=file_name,
            file_path=file_path,
            file_size=file_size,
            file_type=file_type,
            extension=extension
        )
        db.add(db_media)
        db.commit()
        db.refresh(db_media)
        return db_media
    
    def update(self, db: Session, **kwargs) -> 'MediaFile':
        """更新媒体文件信息"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        
        # 更新modify_time
        self.modify_time = datetime.now()
        
        db.commit()
        db.refresh(self)
        return self
    
    def delete(self, db: Session) -> None:
        """删除媒体文件"""
        db.delete(self)
        db.commit()
