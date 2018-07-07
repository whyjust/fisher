from math import floor

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import  TimedJSONWebSignatureSerializer as Serializer

from app.libs.enums import PendingStatus
from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Boolean, Float
from app import login_manager
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.libs.helper import is_isbn_or_key
from flask import current_app

class User(Base, UserMixin):
    '''
    模型属性设置 , UserMixin 记录用户账号的状态
    '''
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    _password = Column('password', String(128), nullable=True)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    '''
    将password方法hash加密只读并将其变为属性访问
    '''
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    '''
    实现当前用户下接受的书籍数/2 <= 发送的书籍数  用户才能进行交易
    '''
    def can_send_drift(self):
        if self.beans < 1:
            return False
        success_gifts_count = Gift.query.filter_by(
            uid=self.id,launched=True).count()
        success_recieve_count = Drift.query.filter_by(
            request_id=self.id,pending=PendingStatus.Success).count()
        return True if floor(success_recieve_count/2) <= floor(success_gifts_count) else False

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if not yushu_book.first:
            return False
        '''
        不允许一个用户同时赠送多本相同的书
        一个用户不可能成为赠送者与索要者

        既不在赠送清单又不在心愿清单才能添加进去
        '''
        gifting = Gift.query.filter_by(uid=self.id,isbn=isbn,launched=False).first()
        wishing = Wish.query.filter_by(uid=self.id,isbn=isbn,launched=False).first()
        if not gifting and not wishing:
            return True
        else:
            return False

    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'id':self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token,new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            if user:
                user.password = new_password
        return True

    @property
    def summary(self):
        return dict(
            nickname = self.nickname,
            beans = self.beans,
            email = self.email,
            send_receive = str(self.send_counter)+ '/' + str(self.receive_counter)
        )


@login_manager.user_loader
def get_user(uid):
    '''
    继承UserMixin,进行用户的回调
    :param uid:
    :return:
    '''
    return User.query.get(int(uid))
