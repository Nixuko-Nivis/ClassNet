from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.schemas import user as user_schemas
from app.services import user_service
from app.utils import security

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.get("/profile", response_model=user_schemas.UserProfileResponse)
def get_user_profile(token: str = Depends(oauth2_scheme)):
    """获取用户个人资料"""
    try:
        user_id = security.verify_token(token)
        user = user_service.get_user_profile(user_id)
        return {
            "code": 200,
            "message": "获取成功",
            "data": user
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌"
        )


@router.put("/profile", response_model=user_schemas.UserProfileResponse)
def update_user_profile(user_data: user_schemas.UserProfileUpdate, token: str = Depends(oauth2_scheme)):
    """更新用户个人资料"""
    try:
        user_id = security.verify_token(token)
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
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌"
        )


@router.put("/password", response_model=user_schemas.PasswordUpdateResponse)
def update_password(password_data: user_schemas.PasswordUpdate, token: str = Depends(oauth2_scheme)):
    """更新用户密码"""
    try:
        user_id = security.verify_token(token)
        user_service.update_password(user_id, password_data.current_password, password_data.new_password)
        return {
            "code": 200,
            "message": "密码修改成功",
            "data": None
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌"
        )
