from flask import current_app

from app.models.base import Base, db
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, func
from sqlalchemy.orm import relationship

from app.spider.yushu_book import YuShuBook


class Gift(Base):
    '''
    gift通过relationship关联到User模型类
    并通过userid外键关联到gift
    '''
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    '''
    判断用户id与礼物对应id是否相等
    '''

    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

    @classmethod
    def recent(cls):
        # 链式调用
        recent_gift = Gift.query.filter_by(launched=False).group_by().order_by(Gift.create_time).limit(
            current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    @classmethod
    def get_user_gift(cls, uid):
        '''
        获取用户赠送清单
        '''
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(db.desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_count(cls, isbn_list):
        '''
        根据传入的isbn中到wish表中计算心愿数量
        '''
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(Wish.launched == False,
                                                                             Wish.isbn.in_(isbn_list),
                                                                             Wish.status == 1).group_by(Wish.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]

        return count_list


from app.models.wish import Wish
