from app.libs.email import send_mail
from app.models.base import db
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.wish import MyWishes
from . import web
from flask_login import login_required,current_user
from flask import flash,redirect,url_for,render_template,request
from app import limiter

@web.route('/my/wish')
def my_wish():
    '''
    心愿清单 : 保存当前用户数据
            1 用户id
            2 心愿清单列表
            3 礼物
    :return:
    '''
    uid = current_user.id
    wish_of_mine = Wish.get_user_wish(uid)
    isbn_list = [wish.isbn for wish in wish_of_mine]
    gift_count_list = Wish.get_gift_count(isbn_list)
    view_model = MyWishes(wish_of_mine,gift_count_list)
    return render_template('my_wish.html',wishes=view_model.wishes)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    '''
    保存到心愿清单  1 确定是否能保存到清单
                2 礼物的isbn  用户id
    :param isbn:
    :return:
    '''
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.uid = current_user.id
            wish.isbn = isbn
            db.session.add(wish)
    else:
        flash('该书已经添加至您的赠送清单或已经存在你的心愿清单,请不要重复添加')
    return redirect(url_for('web.book_detail',isbn=isbn))


def limit_key_prefix():
    isbn = request.args['isbn']
    uid = current_user.id
    return 'satisfy_wish/{}/{}'.format(isbn,uid)

@web.route('/satisfy/wish/<int:wid>')
@login_required
@limiter.limit(key_func=limit_key_prefix)
def satisfy_wish(wid):
    '''
    主动赠送书籍 : 1 向想要这本书的人发送一封邮件
                2 注意 : 接口需要做一定频率的限制
                3 适合写成ajax接口
    :param wid:
    :return:
    '''
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(uid=current_user.id,
                                isbn=wish.isbn).first()
    if not gift:
        flash('还未上传此书，请点击“加入到赠送清单”。添加前,请确保自己可以赠送此书')
    else:
        send_mail(wish.user.email,'有人想要送你一本书','email/satisify_wish.html',wish=wish,gift=gift)
        flash('已向他/她发送了一封邮件，如果他/她愿意接受你的赠送，你将收到一个鱼漂')
    return redirect(url_for('web.book_detail',isbn=wish.isbn))

@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    '''
    从心愿列表中撤销
    :param isbn:
    :return:
    '''
    wish = Wish.query.filter_by(isbn=isbn).first()
    if not wish:
        flash('该心愿不存在,删除失败')
    else:
        with db.auto_commit():
            wish.status = 0
    return redirect(url_for('web.my_wish'))


