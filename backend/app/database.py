from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from app.config import settings

# 创建基础模型类
Base = declarative_base()

# 动态获取数据库引擎
def get_engine():
    """获取数据库引擎"""
    # 获取数据库URL
    DATABASE_URL = settings.database_url
    
    # 确保数据库目录存在
    db_path = DATABASE_URL.replace('sqlite:///', '')
    if not os.path.isabs(db_path):
        # 如果是相对路径，相对于项目根目录解析
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(project_root, db_path)
    
    db_dir = os.path.dirname(db_path)
    os.makedirs(db_dir, exist_ok=True)
    
    # 更新数据库URL为绝对路径
    DATABASE_URL = f'sqlite:///{db_path}'
    
    # 创建数据库引擎
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
    )
    
    return engine

# 动态获取数据库会话
def get_db():
    """获取数据库会话"""
    # 获取最新的引擎
    current_engine = get_engine()
    
    # 创建会话工厂
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=current_engine)
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库，创建所有表"""
    # 导入所有模型，确保它们被注册
    from app.models import user, chat, media
    
    # 获取最新的引擎
    current_engine = get_engine()
    
    # 创建所有表
    Base.metadata.create_all(bind=current_engine)
