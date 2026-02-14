from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import system as system_schemas
from app.services import system_service
from app.api.auth import oauth2_scheme
from app.utils import security
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/status", response_model=system_schemas.SystemStatusResponse)
def get_system_status(token: str = Depends(oauth2_scheme)):
    """获取系统状态"""
    try:
        # 验证令牌
        security.verify_token(token)
        
        status_data = system_service.get_system_status()
        return {
            "code": 200,
            "message": "获取系统状态成功",
            "data": status_data
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取系统状态失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取系统状态失败"
        )


@router.get("/resources", response_model=system_schemas.SystemStatusResponse)
def get_resource_usage(token: str = Depends(oauth2_scheme)):
    """获取资源使用情况"""
    try:
        # 验证令牌
        security.verify_token(token)
        
        resource_data = system_service.get_resource_usage()
        return {
            "code": 200,
            "message": "获取资源使用情况成功",
            "data": resource_data
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取资源使用情况失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取资源使用情况失败"
        )
