import re
from typing import Dict, Any, Optional
from app.models.user import User
from app.utils.security import verify_password, get_password_hash
from app.database import get_db


def get_user_profile(user_id: str) -> Dict[str, Any]:
    """获取用户个人资料"""
    db = next(get_db())
    try:
        user = User.get_by_id(db, int(user_id))
        if not user:
            raise ValueError("用户不存在")
        
        return {
            "user_id": user.id,
            "username": user.username,
            "realname": user.real_name,
            "email": user.email,
            "phone": user.phone,
            "qq": user.qq,
            "wechat": user.wechat,
            "address": user.address,
            "bio": user.bio
        }
    finally:
        db.close()


def update_user_profile(user_id: str, user_data) -> Dict[str, Any]:
    """更新用户个人资料"""
    db = next(get_db())
    try:
        user = User.get_by_id(db, int(user_id))
        if not user:
            raise ValueError("用户不存在")
        
        # 检查用户名是否已存在
        if user_data.username and user_data.username != user.username:
            existing_user = User.get_by_username(db, user_data.username)
            if existing_user:
                raise ValueError("用户名已存在")
        
        # 验证用户名格式
        if user_data.username:
            if len(user_data.username) < 3 or len(user_data.username) > 20:
                raise ValueError("用户名长度应在3-20位之间")
        
        # 验证手机号格式
        if user_data.phone:
            if not re.match(r'^1[3-9]\d{9}$', user_data.phone):
                raise ValueError("手机号格式不正确")
        
        # 验证QQ号格式
        if user_data.qq:
            if not re.match(r'^[1-9]\d{4,10}$', user_data.qq):
                raise ValueError("QQ号格式不正确")
        
        # 验证微信号格式
        if user_data.wechat:
            if not re.match(r'^[a-zA-Z0-9_-]{6,20}$', user_data.wechat):
                raise ValueError("微信号格式不正确（6-20位字母、数字、下划线或连字符）")
        
        # 验证住址长度
        if user_data.address:
            if len(user_data.address) > 100:
                raise ValueError("住址长度不能超过100位")
        
        # 验证个人签名长度
        if user_data.bio:
            if len(user_data.bio) > 200:
                raise ValueError("个人签名长度不能超过200位")
        
        # 更新用户信息 - 包括所有字段，即使是空值
        update_data = {
            "username": user_data.username,
            "phone": user_data.phone,
            "qq": user_data.qq,
            "wechat": user_data.wechat,
            "address": user_data.address,
            "bio": user_data.bio
        }
        
        user = user.update(db, **update_data)
        
        return {
            "user_id": user.id,
            "username": user.username,
            "realname": user.real_name,
            "email": user.email,
            "phone": user.phone,
            "qq": user.qq,
            "wechat": user.wechat,
            "address": user.address,
            "bio": user.bio
        }
    finally:
        db.close()


def update_password(user_id: str, current_password: str, new_password: str) -> None:
    """更新用户密码"""
    db = next(get_db())
    try:
        user = User.get_by_id(db, int(user_id))
        if not user:
            raise ValueError("用户不存在")
        
        # 验证原密码
        hashed_password = str(user.password_hash)
        if not verify_password(current_password, hashed_password):
            raise ValueError("原密码错误")
        
        # 检查新密码长度
        if len(new_password) < 8:
            raise ValueError("新密码长度至少8位")
        
        # 更新密码
        hashed_new_password = get_password_hash(new_password)
        user.update(db, password_hash=hashed_new_password)
    finally:
        db.close()
