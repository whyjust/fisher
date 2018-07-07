from flask import request
from flask import render_template, flash
from flask_login import current_user

from app.form.book import SearchForm
from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookCollection, BookViewModel
from app.view_models.trade import TradeInfo
from . import web


@web.route('/book/search')
def search():
    '''
    搜索函数
    :param: q:[普通关键字 isbn] page,放在request中通过args获取
    :return:
    '''
    '''
    q = request.args['q']
    page = request.args['page']
    '''
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)

        '''return json.dumps(books,default=lambda obj:obj.__dict__,ensure_ascii=True)'''

    else:
        '''return jsonify(form.errors)'''
        flash('您输入的搜索关键字不符合要求,请重新输入')
    return render_template('search_result.html', books=books, form=form)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    '''
    书籍详情页展示: 1 包含书籍的相关信息
                  2 所有请求书籍人信息列表
                  3 所有赠送者信息列表
    :param isbn:
    :return:
    '''
    has_in_gifts = False
    has_in_wishes = False

    '''
    对应数据的详情信息
    '''
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id,isbn=isbn,launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
            has_in_wishes = True
    '''
    所有赠送者清单
    所有索要者清单
    '''
    trade_gifts = Gift.query.filter_by(isbn=isbn,launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn,launched=False).all()
    '''
    展示用户信息,时间
    '''
    trade_wishes_model = TradeInfo(trade_wishes)
    trade_gifts_model = TradeInfo(trade_gifts)

    return render_template('book_detail.html', book=book, wishes=trade_wishes_model, gifts=trade_gifts_model,has_in_gifts=has_in_gifts,has_in_wishes=has_in_wishes)
