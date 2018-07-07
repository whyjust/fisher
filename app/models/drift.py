from sqlalchemy import Column,String,Integer,SmallInteger

from app.libs.enums import PendingStatus
from app.models.base import Base


class Drift(Base):
    '''
    鱼漂:一次具体的交易的信息
    '''
    id = Column(Integer,primary_key=True)

    #邮寄信息
    recipient_name = Column(String(20),nullable=False)
    address = Column(String(100),nullable=False)
    message = Column(String(200))
    mobile = Column(String(20),nullable=False)

    #书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    #请求者信息
    request_id = Column(Integer)
    request_nickname = Column(String(20))

    #赠送者信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))

    #鱼漂的状态
    _pending = Column('pending',SmallInteger,default=1)

    @property
    def pending(self):
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self,status):
        self._pending = status.value

'''
此处有两种方案:
方案1 : 直接在Drift类中存储所有需要的信息,优点是存储之后不可更改,应用场景 历史记录或日志等
方案2 : 有些重复性的信息可以通过关联表查询,优点是减少冗余存储,缺点 用户状态会随用户的改变而发生变动
'''