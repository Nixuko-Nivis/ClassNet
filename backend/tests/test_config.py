import sys
import os

# 设置环境变量，确保测试能正确加载配置
os.environ.setdefault('SECRET_KEY', 'test_secret_key_for_config_testing')

# 添加backend目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import get_settings, reload_settings


def test_config_loading():
    """测试配置加载功能"""
    settings = get_settings()
    
    # 验证基本配置项
    try:
        assert settings.server_host == "0.0.0.0"
        assert settings.server_port == 8000
        assert settings.database_url == "sqlite:///./data/database/classnet.db"
        assert settings.algorithm == "HS256"
        assert settings.access_token_expire_minutes == 1440
        assert settings.redis_url == "redis://localhost:6379"
        assert settings.media_dir == "./data/media"
        assert settings.resource_server_port == 8001
        assert settings.log_level == "INFO"
        assert settings.log_dir == "./data/logs"
        assert settings.cors_origins == ["*"]
        assert settings.request_timeout == 30
        assert settings.max_upload_size == 100 * 1024 * 1024
        print("配置加载测试通过")
        return True
    except AssertionError as e:
        print(f"配置加载测试失败: {e}")
        return False


def test_config_reload():
    """测试配置重载功能"""
    try:
        # 获取初始配置
        initial_settings = get_settings()
        initial_port = initial_settings.server_port
        
        # 重载配置
        reloaded_settings = reload_settings()
        
        # 验证配置重载后对象不同但值相同
        assert initial_settings is not reloaded_settings
        assert reloaded_settings.server_port == initial_port
        print("配置重载测试通过")
        return True
    except AssertionError as e:
        print(f"配置重载测试失败: {e}")
        return False


def test_config_methods():
    """测试配置对象的方法"""
    try:
        settings = get_settings()
        
        # 测试获取访问令牌过期时间
        print("测试获取访问令牌过期时间...")
        expire_time = settings.get_access_token_expire_time()
        assert expire_time.total_seconds() == 1440 * 60
        print("✓ 访问令牌过期时间测试通过")
        
        # 测试获取媒体路径
        print("测试获取媒体路径...")
        media_path = settings.get_media_path()
        assert media_path == "./data/media"
        print(f"✓ 媒体路径测试通过: {media_path}")
        
        import os
        subpath = settings.get_media_path("videos")
        expected_subpath = os.path.normpath("./data/media/videos")
        assert os.path.normpath(subpath) == expected_subpath
        print(f"✓ 媒体子路径测试通过: {subpath}")
        
        # 测试获取日志路径
        print("测试获取日志路径...")
        log_path = settings.get_log_path()
        expected_log_path = os.path.normpath("./data/logs")
        assert os.path.normpath(log_path) == expected_log_path
        print(f"✓ 日志路径测试通过: {log_path}")
        
        log_file_path = settings.get_log_path("app.log")
        expected_log_file_path = os.path.normpath("./data/logs/app.log")
        assert os.path.normpath(log_file_path) == expected_log_file_path
        print(f"✓ 日志文件路径测试通过: {log_file_path}")
        
        # 测试获取配置字典（排除敏感信息）
        print("测试获取配置字典...")
        config_dict = settings.dict()
        assert "secret_key" in config_dict
        assert config_dict["secret_key"] == "******"
        assert "server_host" in config_dict
        assert config_dict["server_host"] == "0.0.0.0"
        print("✓ 配置字典测试通过")
        
        # 测试获取配置JSON
        print("测试获取配置JSON...")
        config_json = settings.json()
        assert "server_host" in config_json
        assert "secret_key" in config_json
        assert "******" in config_json
        print("✓ 配置JSON测试通过")
        
        print("配置方法测试通过")
        return True
    except AssertionError as e:
        print(f"配置方法测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    except Exception as e:
        print(f"配置方法测试发生异常: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test1 = test_config_loading()
    test2 = test_config_reload()
    test3 = test_config_methods()
    
    if test1 and test2 and test3:
        print("所有配置测试通过！")
    else:
        print("部分测试失败！")
