from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas import auth as auth_schemas
from app.services import auth_service
from app.utils import security

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@router.post("/register", response_model=auth_schemas.RegisterResponse)
def register(user_data: auth_schemas.RegisterRequest):
    """用户注册"""
    try:
        # 手动截断密码，确保不超过72字节
        password = user_data.password[:72]
        user = auth_service.register(
            username=user_data.username,
            password=password,
            realname=user_data.realname,
            email=user_data.email
        )
        return {
            "code": 200,
            "message": "注册成功",
            "data": user
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=auth_schemas.LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """用户登录"""
    try:
        user = auth_service.login(
            username=form_data.username,
            password=form_data.password
        )
        access_token = security.create_access_token(
            data={"sub": str(user["user_id"])}
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


@router.post("/change-password", response_model=auth_schemas.ChangePasswordResponse)
def change_password(
    password_data: auth_schemas.ChangePasswordRequest,
    token: str = Depends(oauth2_scheme)
):
    """修改密码"""
    try:
        user_id = security.verify_token(token)
        auth_service.change_password(
            user_id=user_id,
            old_password=password_data.old_password,
            new_password=password_data.new_password,
            confirm_password=password_data.confirm_password
        )
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
