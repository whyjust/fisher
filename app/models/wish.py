from app.models.base import Base, db
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String,func,desc
from sqlalchemy.orm import relationship

from app.spider.yushu_book import YuShuBook

class Wish(Base):
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)

    @classmethod
    def get_user_wish(cls, uid):
        '''
        获取用户心愿清单
        '''
        gifts = Wish.query.filter_by(uid=uid, launched=False).order_by(desc(Wish.create_time)).all()
        return gifts

    @classmethod
    def get_gift_count(cls, isbn_list):
        '''
        根据传入的isbn中到Gift表中计算赠送数量
        '''
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(Gift.launched == False,Gift.isbn.in_(isbn_list),Gift.status == 1).group_by(Gift.isbn).all()
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

from app.models.gift import Gift