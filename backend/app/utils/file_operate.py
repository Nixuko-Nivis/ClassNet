import os
import stat
from datetime import datetime
from typing import Dict, Any, Union


def get_file_size_human(file_size: Union[int, float]) -> str:
    """将文件大小转换为人类可读格式"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if file_size < 1024.0:
            return f"{file_size:.2f} {unit}"
        file_size /= 1024.0
    return f"{file_size:.2f} PB"


def get_file_type(file_path: str) -> str:
    """获取文件类型"""
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv']:
        return 'video'
    elif ext in ['.mp3', '.wav', '.ogg', '.flac', '.aac']:
        return 'audio'
    elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
        return 'image'
    elif ext in ['.txt', '.doc', '.docx', '.pdf', '.xls', '.xlsx']:
        return 'document'
    else:
        return 'other'


def get_file_info(file_path: str) -> Dict[str, Any]:
    """获取文件信息"""
    if not os.path.exists(file_path):
        raise ValueError("文件不存在")
    
    # 获取文件基本信息
    stat_info = os.stat(file_path)
    file_name = os.path.basename(file_path)
    file_size = stat_info.st_size
    file_size_human = get_file_size_human(file_size)
    file_type = get_file_type(file_path)
    extension = os.path.splitext(file_path)[1].lstrip('.').lower()
    
    # 获取文件时间信息
    create_time = datetime.fromtimestamp(stat_info.st_ctime)
    modify_time = datetime.fromtimestamp(stat_info.st_mtime)
    
    return {
        "id": str(hash(file_path)),  # 使用文件路径的哈希值作为临时ID
        "file_name": file_name,
        "file_path": file_path,
        "file_size": file_size,
        "file_size_human": file_size_human,
        "file_type": file_type,
        "extension": extension,
        "create_time": create_time.isoformat(),
        "modify_time": modify_time.isoformat()
    }


def list_files(directory: str, file_type: str = "all") -> list:
    """列出目录中的文件"""
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            try:
                if file_type == "all" or get_file_type(file_path) == file_type:
                    files.append(get_file_info(file_path))
            except Exception:
                pass
    return files
