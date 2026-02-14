from typing import Dict, Any, List
import os
import glob
from app.models.media import MediaFile
from app.utils.file_operate import get_file_info as get_file_info_util


def get_videos(page: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """获取视频列表"""
    video_dir = os.path.join("./data/media", "videos")
    videos = []
    
    # 遍历视频目录
    for file_path in glob.glob(os.path.join(video_dir, "*.*")):
        try:
            file_info = get_file_info_util(file_path)
            videos.append(file_info)
        except Exception:
            pass
    
    # 分页处理
    total = len(videos)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_videos = videos[start:end]
    
    return {
        "items": paginated_videos,
        "total": total,
        "page": page,
        "page_size": page_size
    }


def get_audios(page: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """获取音频列表"""
    audio_dir = os.path.join("./data/media", "audios")
    audios = []
    
    # 遍历音频目录
    for file_path in glob.glob(os.path.join(audio_dir, "*.*")):
        try:
            file_info = get_file_info_util(file_path)
            audios.append(file_info)
        except Exception:
            pass
    
    # 分页处理
    total = len(audios)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_audios = audios[start:end]
    
    return {
        "items": paginated_audios,
        "total": total,
        "page": page,
        "page_size": page_size
    }


def get_file_info(path: str) -> Dict[str, Any]:
    """获取文件信息"""
    # 检查文件是否存在
    if not os.path.exists(path):
        raise ValueError("文件不存在")
    
    return get_file_info_util(path)


def search_files(keyword: str, file_type: str = "all", page: int = 1, page_size: int = 20) -> Dict[str, Any]:
    """搜索文件"""
    media_dir = "./data/media"
    files = []
    
    # 根据文件类型确定搜索目录
    if file_type == "video":
        search_dirs = [os.path.join(media_dir, "videos")]
    elif file_type == "audio":
        search_dirs = [os.path.join(media_dir, "audios")]
    elif file_type == "photo":
        search_dirs = [os.path.join(media_dir, "photos")]
    else:
        search_dirs = [
            os.path.join(media_dir, "videos"),
            os.path.join(media_dir, "audios"),
            os.path.join(media_dir, "photos")
        ]
    
    # 搜索文件
    for search_dir in search_dirs:
        for file_path in glob.glob(os.path.join(search_dir, "*.*")):
            if keyword.lower() in os.path.basename(file_path).lower():
                try:
                    file_info = get_file_info_util(file_path)
                    files.append(file_info)
                except Exception:
                    pass
    
    # 分页处理
    total = len(files)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_files = files[start:end]
    
    return {
        "items": paginated_files,
        "total": total,
        "page": page,
        "page_size": page_size
    }
