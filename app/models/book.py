'''
flask在sqlalchemy 中封装了Flask_SQLAlchemy
flask在WTFORMS 中封装了Flask_WTFORMS
'''
from sqlalchemy import Column, Integer, String
from app.models.base import Base

class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)  # 主键自增
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='未名')
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)  # 唯一性
    summary = Column(String(1000))
    image = Column(String(50))

