import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import init_db, get_db
from app.models import User, Message, MediaFile


def test_database_init():
    """测试数据库初始化"""
    print("=== 测试数据库初始化 ===")
    try:
        init_db()
        print("✓ 数据库初始化成功")
        return True
    except Exception as e:
        print(f"✗ 数据库初始化失败: {e}")
        return False


def test_user_crud():
    """测试用户模型的CRUD操作"""
    print("=== 测试用户模型CRUD操作 ===")
    db = next(get_db())
    
    try:
        # 创建用户
        user = User.create(
            db=db,
            username="testuser",
            password_hash="testpasswordhash",
            email="test@example.com",
            real_name="Test User"
        )
        print(f"✓ 创建用户成功: {user.username}")
        
        # 根据ID获取用户
        user_id = int(user.id)
        user_by_id = User.get_by_id(db, user_id)
        assert user_by_id is not None
        assert user_by_id.username == "testuser"
        print("✓ 根据ID获取用户成功")
        
        # 根据用户名获取用户
        user_by_username = User.get_by_username(db, "testuser")
        assert user_by_username is not None
        assert int(user_by_username.id) == user_id
        print("✓ 根据用户名获取用户成功")
        
        # 根据邮箱获取用户
        user_by_email = User.get_by_email(db, "test@example.com")
        assert user_by_email is not None
        assert int(user_by_email.id) == user_id
        print("✓ 根据邮箱获取用户成功")
        
        # 更新用户信息
        updated_user = user.update(db, real_name="Updated Test User")
        assert updated_user.real_name == "Updated Test User"
        print("✓ 更新用户信息成功")
        
        # 获取所有用户
        users = User.get_all(db)
        assert len(users) >= 1
        print("✓ 获取所有用户成功")
        
        # 删除用户
        user.delete(db)
        deleted_user = User.get_by_id(db, user.id)
        assert deleted_user is None
        print("✓ 删除用户成功")
        
        return True
    except Exception as e:
        print(f"✗ 用户CRUD操作失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def test_message_crud():
    """测试消息模型的CRUD操作"""
    print("=== 测试消息模型CRUD操作 ===")
    db = next(get_db())
    
    try:
        # 先创建一个用户
        user = User.create(
            db=db,
            username="testuser2",
            password_hash="testpasswordhash2"
        )
        user_id = int(user.id)
        
        # 创建消息
        message = Message.create(
            db=db,
            room_id="testroom",
            sender_id=user_id,
            content="Hello, this is a test message!"
        )
        message_id = int(message.id)
        print(f"✓ 创建消息成功: {message_id}")
        
        # 根据ID获取消息
        message_by_id = Message.get_by_id(db, message_id)
        assert message_by_id is not None
        assert message_by_id.content == "Hello, this is a test message!"
        print("✓ 根据ID获取消息成功")
        
        # 根据房间ID获取消息
        messages_by_room = Message.get_by_room_id(db, "testroom")
        assert len(messages_by_room) >= 1
        print("✓ 根据房间ID获取消息成功")
        
        # 根据发送者ID获取消息
        messages_by_sender = Message.get_by_sender_id(db, user_id)
        assert len(messages_by_sender) >= 1
        print("✓ 根据发送者ID获取消息成功")
        
        # 更新消息
        updated_message = message.update(db, content="Updated test message")
        assert updated_message.content == "Updated test message"
        print("✓ 更新消息成功")
        
        # 删除消息
        message.delete(db)
        deleted_message = Message.get_by_id(db, message_id)
        assert deleted_message is None
        print("✓ 删除消息成功")
        
        # 清理用户
        user.delete(db)
        
        return True
    except Exception as e:
        print(f"✗ 消息CRUD操作失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def test_media_file_crud():
    """测试媒体文件模型的CRUD操作"""
    print("=== 测试媒体文件模型CRUD操作 ===")
    db = next(get_db())
    
    try:
        # 创建媒体文件
        media_file = MediaFile.create(
            db=db,
            file_name="test.jpg",
            file_path="/test/path/test.jpg",
            file_size=1024,
            file_type="image",
            extension="jpg"
        )
        media_id = int(media_file.id)
        print(f"✓ 创建媒体文件成功: {media_file.file_name}")
        
        # 根据ID获取媒体文件
        media_by_id = MediaFile.get_by_id(db, media_id)
        assert media_by_id is not None
        assert media_by_id.file_name == "test.jpg"
        print("✓ 根据ID获取媒体文件成功")
        
        # 根据路径获取媒体文件
        media_by_path = MediaFile.get_by_path(db, "/test/path/test.jpg")
        assert media_by_path is not None
        assert int(media_by_path.id) == media_id
        print("✓ 根据路径获取媒体文件成功")
        
        # 根据类型获取媒体文件
        media_by_type = MediaFile.get_by_type(db, "image")
        assert len(media_by_type) >= 1
        print("✓ 根据类型获取媒体文件成功")
        
        # 根据扩展名获取媒体文件
        media_by_extension = MediaFile.get_by_extension(db, "jpg")
        assert len(media_by_extension) >= 1
        print("✓ 根据扩展名获取媒体文件成功")
        
        # 获取所有媒体文件
        all_media = MediaFile.get_all(db)
        assert len(all_media) >= 1
        print("✓ 获取所有媒体文件成功")
        
        # 更新媒体文件
        updated_media = media_file.update(db, file_name="updated_test.jpg")
        assert updated_media.file_name == "updated_test.jpg"
        print("✓ 更新媒体文件成功")
        
        # 删除媒体文件
        media_file.delete(db)
        deleted_media = MediaFile.get_by_id(db, media_id)
        assert deleted_media is None
        print("✓ 删除媒体文件成功")
        
        return True
    except Exception as e:
        print(f"✗ 媒体文件CRUD操作失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def test_model_relationships():
    """测试模型之间的关系"""
    print("=== 测试模型关系 ===")
    db = next(get_db())
    
    try:
        # 创建用户
        user = User.create(
            db=db,
            username="testuser3",
            password_hash="testpasswordhash3"
        )
        user_id = int(user.id)
        
        # 创建消息
        message = Message.create(
            db=db,
            room_id="testroom2",
            sender_id=user_id,
            content="Test message for relationship"
        )
        
        # 测试用户和消息的关系
        assert message.sender is not None
        assert int(message.sender.id) == user_id
        assert message.sender.username == "testuser3"
        print("✓ 用户和消息关系测试成功")
        
        # 清理
        message.delete(db)
        user.delete(db)
        
        return True
    except Exception as e:
        print(f"✗ 模型关系测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        db.close()


def main():
    """主测试函数"""
    print("开始测试数据库模型功能完整性...")
    print("=" * 60)
    
    # 运行所有测试
    tests = [
        test_database_init,
        test_user_crud,
        test_message_crud,
        test_media_file_crud,
        test_model_relationships
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 60)
    print(f"测试结果: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有数据库模型测试通过！")
        return True
    else:
        print("⚠ 部分测试未通过，需要检查")
        return False


if __name__ == "__main__":
    main()
