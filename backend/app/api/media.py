from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.schemas import media as media_schemas
from app.services import media_service
from app.api.auth import oauth2_scheme
from app.utils import security

router = APIRouter()


@router.get("/videos", response_model=media_schemas.VideoListResponse)
def get_videos(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    token: str = Depends(oauth2_scheme)
):
    """获取视频列表"""
    try:
        # 验证令牌
        security.verify_token(token)
        
        videos = media_service.get_videos(page=page, page_size=page_size)
        return {
            "code": 200,
            "message": "获取视频列表成功",
            "data": videos
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌"
        )


@router.get("/audios", response_model=media_schemas.AudioListResponse)
def get_audios(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    token: str = Depends(oauth2_scheme)
):
    """获取音频列表"""
    try:
        # 验证令牌
        security.verify_token(token)
        
        audios = media_service.get_audios(page=page, page_size=page_size)
        return {
            "code": 200,
            "message": "获取音频列表成功",
            "data": audios
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌"
        )


@router.get("/fileinfo", response_model=media_schemas.FileInfoResponse)
def get_file_info(
    path: str = Query(..., description="文件路径"),
    token: str = Depends(oauth2_scheme)
):
    """获取文件信息"""
    try:
        # 验证令牌
        security.verify_token(token)
        
        file_info = media_service.get_file_info(path=path)
        return {
            "code": 200,
            "message": "获取文件信息成功",
            "data": file_info
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌"
        )
