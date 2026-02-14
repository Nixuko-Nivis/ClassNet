import logging
import os
from logging.handlers import RotatingFileHandler

# 确保日志目录存在
log_dir = os.path.join("./data", "logs")
os.makedirs(log_dir, exist_ok=True)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler(
            os.path.join(log_dir, "app.log"),
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        ),
        logging.StreamHandler()
    ]
)

# 创建不同模块的日志记录器
def get_logger(name: str) -> logging.Logger:
    """获取日志记录器"""
    return logging.getLogger(name)

# 示例日志记录器
app_logger = get_logger("app")
auth_logger = get_logger("auth")
media_logger = get_logger("media")
chat_logger = get_logger("chat")
weather_logger = get_logger("weather")
system_logger = get_logger("system")
