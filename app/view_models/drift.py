from app.libs.enums import PendingStatus

class DriftCollection:
   '''
   多组鱼漂的交易记录详情页面
   处理多个鱼漂数据,转成单个数据放在列表中
   '''
   def __init__(self,drifts,current_user_id):
       self.data = []
       self.__parse(drifts,current_user_id)

   def __parse(self,drifts,current_user_id):
        for drift in drifts:
            temp = DriftViewModel(drift,current_user_id)
            self.data.append(temp.data)


class DriftViewModel:
    '''
    单组鱼漂的交易记录详情页面
    处理单个鱼漂数据的信息
    '''
    def __init__(self,drift,current_user_id):
        self.data = {}
        self.data = self.__parse(drift,current_user_id)

    @staticmethod
    def request_or_gifter(drift, current_user_id):
        if drift.request_id == current_user_id:
            you_are = 'requester'
        else:
            you_are = 'gifter'
        return you_are

    def __parse(self,drift,current_user_id):
        '''
        单组数据 : 需要区分 : 请求者 or 赠送者
        :param drift:
        :param current_user_id:
        :return:
        '''
        you_are = self.request_or_gifter(drift,current_user_id)
        pending_status = PendingStatus.pending_str(drift.pending,you_are)

        r = {
            'you_are':you_are,
            'drift_id':drift.id,
            'book_title':drift.book_title,
            'book_author':drift.book_author,
            'book_img':drift.book_img,
            'date':drift.create_datetime.strftime('%Y-%m-%d'),
            'operator':drift.request_nickname if you_are != 'requester' else drift.gifter_nickname,
            'message':drift.message,
            'address':drift.address,
            'status_str':pending_status,
            'recipient_name':drift.recipient_name,
            'mobile':drift.mobile,
            'status':drift.pending
        }
        return r
