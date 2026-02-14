from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import weather as weather_schemas
from app.services import weather_service
from app.api.auth import oauth2_scheme
from app.utils import security
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=weather_schemas.WeatherResponse)
def get_weather(token: str = Depends(oauth2_scheme)):
    """获取天气信息"""
    try:
        # 验证令牌
        security.verify_token(token)
        
        weather_data = weather_service.get_weather()
        return {
            "code": 200,
            "message": "获取天气信息成功",
            "data": weather_data
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取天气信息时发生错误: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取天气信息失败"
        )
