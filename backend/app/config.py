from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any
import os
import json
from datetime import timedelta


class Settings(BaseSettings):
    """应用配置"""
    # 服务器配置
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    
    # 数据库配置
    database_url: str = "sqlite:///./data/database/classnet_new.db"
    
    # 认证配置
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    
    # Redis配置
    redis_url: str = "redis://localhost:6379"
    
    # 媒体配置
    media_dir: str = "./data/media"
    
    # 资源服务器配置
    resource_server_port: int = 8001
    
    # 日志配置
    log_level: str = "INFO"
    log_dir: str = "./data/logs"
    
    # CORS配置
    cors_origins: list = ["*"]
    
    # 性能配置
    request_timeout: int = 30
    max_upload_size: int = 100 * 1024 * 1024  # 100MB
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    def get_access_token_expire_time(self) -> timedelta:
        """获取访问令牌过期时间"""
        return timedelta(minutes=self.access_token_expire_minutes)
    
    def get_media_path(self, subpath: Optional[str] = None) -> str:
        """获取媒体文件路径"""
        # 确保媒体目录路径是绝对路径
        media_dir = self.media_dir
        if not os.path.isabs(media_dir):
            # 如果是相对路径，相对于项目根目录解析
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            media_dir = os.path.join(project_root, media_dir)
        
        # 确保目录存在
        os.makedirs(media_dir, exist_ok=True)
        
        if subpath:
            return os.path.join(media_dir, subpath)
        return media_dir
    
    def get_log_path(self, filename: Optional[str] = None) -> str:
        """获取日志文件路径"""
        os.makedirs(self.log_dir, exist_ok=True)
        if filename:
            return os.path.join(self.log_dir, filename)
        return self.log_dir
    
    def dict(self, **kwargs) -> Dict[str, Any]:
        """返回配置字典，排除敏感信息"""
        config_dict = super().dict(**kwargs)
        # 移除敏感信息
        if "secret_key" in config_dict:
            config_dict["secret_key"] = "******"
        return config_dict
    
    def json(self, **kwargs) -> str:
        """返回配置JSON字符串，排除敏感信息"""
        return json.dumps(self.dict(**kwargs), ensure_ascii=False, indent=2)


# 全局配置实例
settings = Settings()


def get_settings() -> Settings:
    """获取配置实例"""
    return settings


def reload_settings() -> Settings:
    """重新加载配置"""
    global settings
    settings = Settings()
    return settings

