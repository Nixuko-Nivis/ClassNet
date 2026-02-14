import re
import json
import os
from typing import Dict, Any, Optional
from app.models.user import User
from app.utils.security import verify_password, get_password_hash
from app.database import get_db

# 加载统一用户数据
# 从项目根目录加载统一用户数据
current_file = os.path.abspath(__file__)
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
project_root = os.path.dirname(backend_dir)
UNIFIED_USER_DATA_PATH = os.path.join(project_root, 'data', 'database', 'unified_user_data.json')

def load_unified_user_data() -> Dict[str, Any]:
    """加载统一用户数据"""
    try:
        with open(UNIFIED_USER_DATA_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载统一用户数据失败: {e}")
        return {"user_ids": {}}

# 缓存统一用户数据
unified_user_data = load_unified_user_data()


def get_user_profile(user_id: str) -> Dict[str, Any]:
    """获取用户个人资料"""
    db = next(get_db())
    try:
        # 尝试将用户ID转换为整数
        user = None
        try:
            user_id_int = int(user_id)
            user = User.get_by_id(db, user_id_int)
        except ValueError:
            pass
        
        # 如果通过ID找不到用户，尝试从统一用户数据中查找对应的真实用户ID
        if not user:
            # 遍历统一用户数据，查找匹配的真实姓名
            for real_name, formatted_id in unified_user_data.get("user_ids", {}).items():
                if formatted_id == user_id:
                    # 找到匹配的格式化ID，根据真实姓名查找用户
                    user = User.get_by_real_name(db, real_name)
                    break
        
        if not user:
            raise ValueError("用户不存在")
        
        # 获取统一用户数据中的格式化ID
        formatted_user_id = user.id
        if user.real_name:
            formatted_user_id = unified_user_data.get("user_ids", {}).get(user.real_name, user.id)
        
        return {
            "user_id": formatted_user_id,
            "username": user.username,
            "realname": user.real_name,
            "email": user.email,
            "phone": user.phone,
            "qq": user.qq,
            "wechat": user.wechat,
            "address": user.address,
            "bio": user.bio,
            "birthday": user.birthday
        }
    finally:
        db.close()


def update_user_profile(user_id: str, user_data) -> Dict[str, Any]:
    """更新用户个人资料"""
    db = next(get_db())
    try:
        # 尝试将用户ID转换为整数
        try:
            user_id_int = int(user_id)
            user = User.get_by_id(db, user_id_int)
        except ValueError:
            # 如果转换失败，尝试从统一用户数据中查找对应的真实用户ID
            user = None
            # 遍历统一用户数据，查找匹配的真实姓名
            for real_name, formatted_id in unified_user_data.get("user_ids", {}).items():
                if formatted_id == user_id:
                    # 找到匹配的格式化ID，根据真实姓名查找用户
                    user = User.get_by_real_name(db, real_name)
                    break
        
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
        
        # 验证生日格式（可选）
        if user_data.birthday:
            # 简单的日期格式验证（YYYY-MM-DD）
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', user_data.birthday):
                raise ValueError("生日格式不正确，应为 YYYY-MM-DD")
        
        # 更新用户信息 - 包括所有字段，即使是空值
        update_data = {
            "username": user_data.username,
            "phone": user_data.phone,
            "qq": user_data.qq,
            "wechat": user_data.wechat,
            "address": user_data.address,
            "bio": user_data.bio,
            "birthday": user_data.birthday
        }
        
        user = user.update(db, **update_data)
        
        # 获取统一用户数据中的格式化ID
        formatted_user_id = user.id
        if user.real_name:
            formatted_user_id = unified_user_data.get("user_ids", {}).get(user.real_name, user.id)
        
        return {
            "user_id": formatted_user_id,
            "username": user.username,
            "realname": user.real_name,
            "email": user.email,
            "phone": user.phone,
            "qq": user.qq,
            "wechat": user.wechat,
            "address": user.address,
            "bio": user.bio,
            "birthday": user.birthday
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


def get_all_users() -> Dict[str, Any]:
    """获取所有用户列表"""
    db = next(get_db())
    try:
        users = User.get_all(db)
        user_list = []
        
        for user in users:
            # 获取统一用户数据中的格式化ID
            formatted_user_id = user.id
            if user.real_name:
                formatted_user_id = unified_user_data.get("user_ids", {}).get(user.real_name, user.id)
            
            user_list.append({
                "user_id": formatted_user_id,
                "username": user.username,
                "realname": user.real_name,
                "email": user.email,
                "phone": user.phone,
                "qq": user.qq,
                "wechat": user.wechat,
                "address": user.address,
                "bio": user.bio,
                "birthday": user.birthday
            })
        
        return {
            "users": user_list,
            "total": len(user_list)
        }
    finally:
        db.close()


def delete_user(user_id: str) -> None:
    """删除用户"""
    db = next(get_db())
    try:
        # 尝试将用户ID转换为整数
        try:
            user_id_int = int(user_id)
            user = User.get_by_id(db, user_id_int)
        except ValueError:
            # 如果转换失败，尝试从统一用户数据中查找对应的真实用户ID
            user = None
            # 遍历统一用户数据，查找匹配的真实姓名
            for real_name, formatted_id in unified_user_data.get("user_ids", {}).items():
                if formatted_id == user_id:
                    # 找到匹配的格式化ID，根据真实姓名查找用户
                    user = User.get_by_real_name(db, real_name)
                    break
        
        if not user:
            raise ValueError("用户不存在")
        
        user.delete(db)
    finally:
        db.close()
