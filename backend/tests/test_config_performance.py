import sys
import os
import time

# 设置环境变量
os.environ.setdefault('SECRET_KEY', 'test_secret_key_for_performance_testing')

# 添加backend目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import get_settings, reload_settings


def test_config_loading_performance():
    """测试配置加载性能"""
    print("测试配置加载性能...")
    
    # 测试多次加载配置的时间
    start_time = time.time()
    iterations = 1000
    
    for i in range(iterations):
        settings = get_settings()
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / iterations * 1000  # 转换为毫秒
    
    print(f"配置加载性能测试: {iterations}次加载耗时 {total_time:.3f} 秒")
    print(f"平均每次加载耗时: {avg_time:.3f} 毫秒")
    
    # 性能阈值检查
    if avg_time < 1.0:
        print("✓ 配置加载性能优秀")
    elif avg_time < 5.0:
        print("✓ 配置加载性能良好")
    else:
        print("⚠ 配置加载性能需要优化")
    
    return avg_time


def test_config_reload_performance():
    """测试配置重载性能"""
    print("\n测试配置重载性能...")
    
    # 测试多次重载配置的时间
    start_time = time.time()
    iterations = 100
    
    for i in range(iterations):
        settings = reload_settings()
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / iterations * 1000  # 转换为毫秒
    
    print(f"配置重载性能测试: {iterations}次重载耗时 {total_time:.3f} 秒")
    print(f"平均每次重载耗时: {avg_time:.3f} 毫秒")
    
    # 性能阈值检查
    if avg_time < 10.0:
        print("✓ 配置重载性能优秀")
    elif avg_time < 50.0:
        print("✓ 配置重载性能良好")
    else:
        print("⚠ 配置重载性能需要优化")
    
    return avg_time


def test_config_compatibility():
    """测试配置管理模块与其他模块的兼容性"""
    print("\n测试配置兼容性...")
    
    try:
        # 测试配置对象是否能被其他模块正常使用
        settings = get_settings()
        
        # 测试配置项是否能被正确访问
        assert hasattr(settings, 'server_host')
        assert hasattr(settings, 'server_port')
        assert hasattr(settings, 'database_url')
        assert hasattr(settings, 'secret_key')
        assert hasattr(settings, 'algorithm')
        assert hasattr(settings, 'access_token_expire_minutes')
        assert hasattr(settings, 'redis_url')
        assert hasattr(settings, 'media_dir')
        assert hasattr(settings, 'resource_server_port')
        assert hasattr(settings, 'log_level')
        assert hasattr(settings, 'log_dir')
        assert hasattr(settings, 'cors_origins')
        assert hasattr(settings, 'request_timeout')
        assert hasattr(settings, 'max_upload_size')
        
        # 测试配置方法是否能被正确调用
        assert callable(getattr(settings, 'get_access_token_expire_time', None))
        assert callable(getattr(settings, 'get_media_path', None))
        assert callable(getattr(settings, 'get_log_path', None))
        assert callable(getattr(settings, 'dict', None))
        assert callable(getattr(settings, 'json', None))
        
        print("✓ 配置兼容性测试通过")
        return True
    except Exception as e:
        print(f"✗ 配置兼容性测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_config_edge_cases():
    """测试配置管理模块的边界情况"""
    print("\n测试配置边界情况...")
    
    try:
        settings = get_settings()
        
        # 测试空路径参数
        media_path = settings.get_media_path("")
        assert media_path == settings.media_dir
        print("✓ 空路径参数测试通过")
        
        # 测试多级路径
        multi_path = settings.get_media_path(r"videos\hd\2026")
        assert "videos" in multi_path
        assert "hd" in multi_path
        assert "2026" in multi_path
        print("✓ 多级路径测试通过")
        
        # 测试日志目录自动创建
        log_path = settings.get_log_path()
        assert os.path.exists(log_path)
        print("✓ 日志目录自动创建测试通过")
        
        # 测试配置字典的敏感性
        config_dict = settings.dict()
        assert config_dict.get('secret_key') == "******"
        print("✓ 配置敏感信息保护测试通过")
        
        return True
    except Exception as e:
        print(f"✗ 配置边界情况测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=== 配置管理模块性能和兼容性测试 ===")
    
    # 运行性能测试
    load_perf = test_config_loading_performance()
    reload_perf = test_config_reload_performance()
    
    # 运行兼容性测试
    compat_result = test_config_compatibility()
    edge_result = test_config_edge_cases()
    
    print("\n=== 测试结果汇总 ===")
    print(f"配置加载性能: {load_perf:.3f} ms/次")
    print(f"配置重载性能: {reload_perf:.3f} ms/次")
    print(f"兼容性测试: {'通过' if compat_result else '失败'}")
    print(f"边界情况测试: {'通过' if edge_result else '失败'}")
    
    if load_perf < 5.0 and reload_perf < 50.0 and compat_result and edge_result:
        print("\n🎉 所有性能和兼容性测试通过！")
    else:
        print("\n⚠ 部分测试未通过，需要进一步优化")
