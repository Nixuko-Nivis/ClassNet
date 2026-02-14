from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.params import Form
from app.schemas import user as user_schemas
from app.schemas import auth as auth_schemas
from app.services import user_service, auth_service
from app.utils import security

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/admin/login")

# 后台管理系统的验证密码
ADMIN_VERIFICATION_PASSWORD = "kjtpcyb07"


def verify_admin_access(token: str = Depends(oauth2_scheme)):
    """验证后台管理访问权限"""
    try:
        user_id = security.verify_token(token)
        # 这里可以添加更严格的权限检查，比如检查用户是否为管理员
        return user_id
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/login", response_model=auth_schemas.LoginResponse)
def admin_login(form_data: OAuth2PasswordRequestForm = Depends()):
    """后台管理系统登录"""
    try:
        # 验证用户名和密码
        user = auth_service.login(
            username=form_data.username,
            password=form_data.password
        )
        
        # 生成访问令牌
        access_token = security.create_access_token(
            data={"sub": str(user["user_id"]), "is_admin": True}
        )
        
        return {
            "code": 200,
            "message": "登录成功",
            "data": {
                "access_token": access_token,
                "token_type": "bearer",
                "user": user
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.post("/verify-password")
def verify_admin_password(password: str = Form(...)):
    """验证后台管理密码"""
    if password != ADMIN_VERIFICATION_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="密码错误"
        )
    return {
        "code": 200,
        "message": "密码验证成功",
        "data": None
    }


@router.get("/users", response_model=user_schemas.UserListResponse)
def get_all_users(token: str = Depends(verify_admin_access)):
    """获取所有用户列表"""
    try:
        users = user_service.get_all_users()
        return {
            "code": 200,
            "message": "获取成功",
            "data": users
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/users/{user_id}", response_model=user_schemas.UserProfileResponse)
def get_user_by_id(user_id: str, token: str = Depends(verify_admin_access)):
    """根据ID获取用户信息"""
    try:
        user = user_service.get_user_profile(user_id)
        return {
            "code": 200,
            "message": "获取成功",
            "data": user
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/users/{user_id}", response_model=user_schemas.UserProfileResponse)
def update_user(user_id: str, user_data: user_schemas.UserProfileUpdate, token: str = Depends(verify_admin_access)):
    """更新用户信息"""
    try:
        user = user_service.update_user_profile(user_id, user_data)
        return {
            "code": 200,
            "message": "更新成功",
            "data": user
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/users/{user_id}")
def delete_user(user_id: str, token: str = Depends(verify_admin_access)):
    """删除用户"""
    try:
        user_service.delete_user(user_id)
        return {
            "code": 200,
            "message": "删除成功",
            "data": None
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
