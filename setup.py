# setup.py

from sqlalchemy import create_engine
from models import Base
from config import DATABASE_URL

# 创建数据库引擎
engine = create_engine(DATABASE_URL)

def init_db():
    # 创建所有定义的表
    Base.metadata.create_all(bind=engine)
    print("数据库初始化完成。")

if __name__ == '__main__':
    init_db()
