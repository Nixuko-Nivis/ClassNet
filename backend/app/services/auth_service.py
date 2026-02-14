from typing import Optional, Dict, Any
from app.models.user import User
from app.utils.security import verify_password, get_password_hash
from app.database import get_db


import json
import os


def load_predefined_names():
    """加载预定义的姓名列表"""
    json_path = os.path.join(os.path.dirname(__file__), '../../../data/database/unified_user_data.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('names', [])
    except Exception as e:
        print(f"加载预定义姓名列表失败: {e}")
        return []


def register(username: str, password: str, realname: str, email: Optional[str] = None) -> Dict[str, Any]:
    """用户注册"""
    db = next(get_db())
    try:
        # 检查用户名是否已存在
        existing_user = User.get_by_username(db, username)
        if existing_user:
            raise ValueError("用户名已存在")
        
        # 检查邮箱是否已存在
        if email:
            existing_email = User.get_by_email(db, email)
            if existing_email:
                raise ValueError("邮箱已被注册")
        
        # 检查密码长度
        if len(password) < 8:
            raise ValueError("密码长度至少8位")
        
        # 验证真实姓名是否在预定义列表中
        predefined_names = load_predefined_names()
        if predefined_names and realname not in predefined_names:
            raise ValueError("真实姓名不在预定义列表中")
        
        # 创建新用户
        hashed_password = get_password_hash(password)
        user = User.create(
            db=db,
            username=username,
            password_hash=hashed_password,
            real_name=realname,
            email=email
        )
        
        if not user:
            raise ValueError("用户创建失败")
        
        return {
            "user_id": user.id,
            "username": user.username,
            "realname": user.real_name,
            "email": user.email
        }
    finally:
        db.close()


def login(username: str, password: str) -> Dict[str, Any]:
    """用户登录"""
    db = next(get_db())
    try:
        # 查找用户 - 先尝试通过用户名查找
        user = User.get_by_username(db, username)
        # 如果通过用户名找不到，尝试通过真实姓名查找
        if not user:
            user = User.get_by_real_name(db, username)
        if not user:
            raise ValueError("用户名或密码错误")
        
        # 验证密码
        hashed_password = str(user.password_hash)
        if not verify_password(password, hashed_password):
            raise ValueError("用户名或密码错误")
        
        return {
            "user_id": user.id,
            "username": user.username,
            "realname": user.real_name,
            "email": user.email
        }
    finally:
        db.close()


def change_password(user_id: str, old_password: str, new_password: str, confirm_password: str) -> None:
    """修改密码"""
    db = next(get_db())
    try:
        # 查找用户
        user = User.get_by_id(db, int(user_id))
        if not user:
            raise ValueError("用户不存在")
        
        # 验证旧密码
        hashed_password = str(user.password_hash)
        if not verify_password(old_password, hashed_password):
            raise ValueError("旧密码错误")
        
        # 检查新密码长度
        if len(new_password) < 8:
            raise ValueError("新密码长度至少8位")
        
        # 确认密码
        if new_password != confirm_password:
            raise ValueError("两次输入的密码不一致")
        
        # 更新密码
        hashed_password = get_password_hash(new_password)
        user.update(db, password_hash=hashed_password)
    finally:
        db.close()


def verify_token(token: str) -> str:
    """验证令牌"""
    from app.utils.security import verify_token as verify_jwt_token
    return verify_jwt_token(token)
