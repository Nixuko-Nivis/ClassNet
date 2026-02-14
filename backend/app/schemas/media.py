from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class MediaFileBase(BaseModel):
    """媒体文件基础模型"""
    file_name: str = Field(..., description="文件名")
    file_size: int = Field(..., gt=0, description="文件大小")
    file_type: str = Field(..., description="文件类型")
    extension: str = Field(..., description="文件扩展名")


class MediaFileCreate(MediaFileBase):
    """媒体文件创建模型"""
    file_path: str = Field(..., description="文件路径")


class MediaFileUpdate(BaseModel):
    """媒体文件更新模型"""
    file_name: Optional[str] = Field(None, description="文件名")
    file_type: Optional[str] = Field(None, description="文件类型")
    extension: Optional[str] = Field(None, description="文件扩展名")


class MediaFileInDB(MediaFileBase):
    """数据库中的媒体文件模型"""
    id: int
    file_path: str
    create_time: datetime
    modify_time: datetime
    
    class Config:
        from_attributes = True


class MediaFile(MediaFileBase):
    """媒体文件响应模型"""
    id: int
    file_path: str
    create_time: datetime
    modify_time: datetime
    
    class Config:
        from_attributes = True


class MediaFileList(BaseModel):
    """媒体文件列表响应模型"""
    files: list[MediaFile]
    total: int


class VideoInfo(BaseModel):
    """视频信息模型"""
    file_name: str
    file_path: str
    file_size: int
    duration: Optional[str] = None
    resolution: Optional[str] = None


class AudioInfo(BaseModel):
    """音频信息模型"""
    file_name: str
    file_path: str
    file_size: int
    duration: Optional[str] = None


class VideoListResponse(BaseModel):
    """视频列表响应模型"""
    code: int
    message: str
    data: dict


class AudioListResponse(BaseModel):
    """音频列表响应模型"""
    code: int
    message: str
    data: dict


class FileInfoResponse(BaseModel):
    """文件信息响应模型"""
    code: int
    message: str
    data: dict
