from app.models.base import db
from app.spider.yushu_book import YuShuBook
from app.models.book import Book
from app.view_models.book import BookViewModel

'''调用API因此book模型不做存储功能'''
# class SQL_save_book(object):
#     def __init__(self,isbn):
#         self.isbn = isbn
#
#     def yushu_isbn(self):
#         book = YuShuBook().search_by_isbn(self.isbn)
#         self.save_yushu(book)
#
#     def save_yushu(self,book):
#         if not SQL_save_book.has_existed(self.isbn):
#             with db.auto_commit():
#                 book_obj = Book()
#                 book_model = book_obj.set_attrs(BookViewModel(book).__dict__)
#                 db.session.add(book_model)
#             return book_model
#
#     def has_existed(self):
#         book = Book.query.filter_by(isbn=self.isbn).first()
#         if book:
#             return book
#         else:
#             return False


