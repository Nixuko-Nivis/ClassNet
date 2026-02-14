from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class RegisterRequest(BaseModel):
    """注册请求"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=8, max_length=72, description="密码")
    realname: str = Field(..., min_length=2, max_length=50, description="真实姓名")
    email: Optional[str] = Field(None, description="邮箱")


class RegisterResponse(BaseModel):
    """注册响应"""
    code: int
    message: str
    data: dict


class LoginResponse(BaseModel):
    """登录响应"""
    code: int
    message: str
    data: dict


class ChangePasswordRequest(BaseModel):
    """修改密码请求"""
    old_password: str = Field(..., description="旧密码")
    new_password: str = Field(..., min_length=8, max_length=72, description="新密码")
    confirm_password: str = Field(..., description="确认密码")


class ChangePasswordResponse(BaseModel):
    """修改密码响应"""
    code: int
    message: str
    data: Optional[dict] = None
