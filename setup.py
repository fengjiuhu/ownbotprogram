# setup.py

from db import engine
from models import Base

def init_db():
    Base.metadata.create_all(bind=engine)
    print("数据库初始化完成。")

if __name__ == '__main__':
    init_db()
