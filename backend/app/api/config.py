from fastapi import APIRouter, Depends, HTTPException, status
from app.api.auth import oauth2_scheme
from app.utils import security
from app.config import get_settings, reload_settings
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter()


class ConfigResponse(BaseModel):
    """配置响应"""
    code: int
    message: str
    data: Dict[str, Any]


class ConfigUpdateRequest(BaseModel):
    """配置更新请求"""
    config: Dict[str, Any]


@router.get("/", response_model=ConfigResponse)
def get_config(token: str = Depends(oauth2_scheme)):
    """获取当前配置"""
    try:
        # 验证令牌
        security.verify_token(token)
        
        settings = get_settings()
        config_dict = settings.dict()
        
        return {
            "code": 200,
            "message": "获取配置成功",
            "data": config_dict
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌"
        )


@router.post("/reload", response_model=ConfigResponse)
def reload_config(token: str = Depends(oauth2_scheme)):
    """重新加载配置"""
    try:
        # 验证令牌
        security.verify_token(token)
        
        settings = reload_settings()
        config_dict = settings.dict()
        
        return {
            "code": 200,
            "message": "配置重新加载成功",
            "data": config_dict
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌"
        )
