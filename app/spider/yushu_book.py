from flask import current_app
from app.libs.httper import Http

class YuShuBook:
    '''
    模型层: mvc中 M层
    '''
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'
    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self,isbn):
        url = self.isbn_url.format(isbn) #或者self.isbn_url.format(isbn)
        result = Http.get(url)          #dict
        self.__fill_single(result)

    def search_by_keyword(self,keyword,page=1):
        url = self.keyword_url.format(keyword,current_app.config.get('PER_PAGE'),self.calulate_start(page))
        result = Http.get(url)
        self.__fill_collection(result)

    def __fill_single(self,data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self,data):
        if data:
            self.total = data['total']
            self.books = data['books']

    def calulate_start(self,page):
        return (page-1)* current_app.config.get('PER_PAGE')


    @property
    def first(self):
        return self.books[0] if self.total>=1 else None
