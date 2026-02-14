from typing import Dict, Any
import datetime

# 尝试导入psutil
psutil_available = False
try:
    import psutil
    psutil_available = True
except ImportError:
    pass


def get_system_status() -> Dict[str, Any]:
    """获取系统状态"""
    # 模拟在线用户数和今日访问量
    online_users = 10
    today_visits = 100
    
    # 获取服务器时间
    server_time = datetime.datetime.now().isoformat()
    
    if psutil_available:
        # 获取CPU使用率
        cpu_usage = psutil.cpu_percent(interval=1)
        
        # 获取内存使用率
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        
        # 获取磁盘使用率
        disk = psutil.disk_usage('/')
        disk_usage = disk.percent
    else:
        # 提供模拟数据
        cpu_usage = 25.5
        memory_usage = 45.2
        disk_usage = 30.8
    
    return {
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "disk_usage": disk_usage,
        "online_users": online_users,
        "today_visits": today_visits,
        "server_time": server_time
    }


def get_resource_usage() -> Dict[str, Any]:
    """获取资源使用情况"""
    if psutil_available:
        # 获取详细的资源使用情况
        cpu_info = {
            "percent": psutil.cpu_percent(interval=1),
            "count": psutil.cpu_count(logical=True)
        }
        
        memory_info = {
            "percent": psutil.virtual_memory().percent,
            "total": psutil.virtual_memory().total / 1024 / 1024 / 1024,  # GB
            "available": psutil.virtual_memory().available / 1024 / 1024 / 1024  # GB
        }
        
        disk_info = {
            "percent": psutil.disk_usage('/').percent,
            "total": psutil.disk_usage('/').total / 1024 / 1024 / 1024,  # GB
            "free": psutil.disk_usage('/').free / 1024 / 1024 / 1024  # GB
        }
    else:
        # 提供模拟数据
        cpu_info = {
            "percent": 25.5,
            "count": 4
        }
        
        memory_info = {
            "percent": 45.2,
            "total": 8.0,
            "available": 4.4
        }
        
        disk_info = {
            "percent": 30.8,
            "total": 500.0,
            "free": 346.0
        }
    
    return {
        "cpu": cpu_info,
        "memory": memory_info,
        "disk": disk_info
    }
