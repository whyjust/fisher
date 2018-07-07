from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import Column, Integer, SmallInteger
from contextlib import contextmanager
from datetime import datetime


class SQLAlchemy(_SQLAlchemy):
    '''
    封装了数据库的自动提交回滚
    '''
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class Query(BaseQuery):
    '''
    自定义基类(继承,初始化),重写filter_by方法
    '''

    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)

db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    '''
    该模型表不想在数据库创建,添加__abstract__ = True不会创建该表
    '''
    __abstract__ = True
    '''类变量在类开始的时候就已经确定了'''
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        '''实例变量保证创建时间的准确性'''
        self.create_time = int(datetime.now().timestamp())

    def delete(self):
        self.status = 0

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None
