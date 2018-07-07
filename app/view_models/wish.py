from .book import BookViewModel

class MyWishes:
    '''
    心愿清单对数据进行处理:返回[{wishes_count,book,id}]数据结构,主要是方便模板渲染
    '''

    def __init__(self,gifts_of_mine,wish_count_list):
        self.wishes = []
        self.__gifts_of_mine = gifts_of_mine
        self.__wish_count_list = wish_count_list
        self.wishes = self.__parse()

    def __parse(self):
        temp_gifts = []
        for gift in self.__gifts_of_mine:
            my_gift = self.__matching(gift)
            temp_gifts.append(my_gift)
        return temp_gifts

    def __matching(self,gift):
        count = 0
        for wish_count in self.__wish_count_list:
            if gift.isbn == wish_count['isbn']:
                count = wish_count['count']
        r = {
            'wishes_count':count,
            'book':BookViewModel(gift.book),
            'id':gift.id
        }
        return r



