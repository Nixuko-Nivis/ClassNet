from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime


class UserProfileUpdate(BaseModel):
    """更新用户个人资料请求"""
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="用户名")
    phone: Optional[str] = Field(None, description="手机号")
    qq: Optional[str] = Field(None, description="QQ号")
    wechat: Optional[str] = Field(None, description="微信号")
    address: Optional[str] = Field(None, description="住址")
    bio: Optional[str] = Field(None, description="个人签名")
    birthday: Optional[str] = Field(None, description="生日")


class UserProfileResponse(BaseModel):
    """用户个人资料响应"""
    code: int
    message: str
    data: Dict[str, Any]


class PasswordUpdate(BaseModel):
    """更新密码请求"""
    current_password: str = Field(..., description="原密码")
    new_password: str = Field(..., min_length=8, max_length=72, description="新密码")


class PasswordUpdateResponse(BaseModel):
    """更新密码响应"""
    code: int
    message: str
    data: Optional[Dict[str, Any]] = None


class UserListResponse(BaseModel):
    """用户列表响应"""
    code: int
    message: str
    data: Dict[str, Any]
