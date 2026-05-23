# 导入必要的模块
from sqlalchemy import create_engine  # 导入SQLAlchemy的create_engine函数，用于创建数据库引擎
from sqlalchemy.orm import sessionmaker, declarative_base  # 导入sessionmaker和declarative_base，用于创建会话和声明基类

# 从应用配置模块导入设置
from app.config import settings

# 创建数据库引擎，使用配置中的数据库URL，设置echo为False表示不打印SQL语句
engine = create_engine(settings.database_url, echo=False)
# 创建会话工厂，配置为不自动提交和自动刷新，并绑定到数据库引擎
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 创建SQLAlchemy的基类，用于模型继承
Base = declarative_base()


# 定义获取数据库会话的函数，使用生成器模式
def get_db():
    # 创建新的数据库会话
    db = SessionLocal()
    try:
        # 使用yield返回会话，供调用者使用
        yield db
    finally:
        # 确保在函数执行完毕后关闭数据库会话
        db.close()
