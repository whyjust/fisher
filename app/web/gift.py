from flask_login import login_required, current_user
from flask import current_app, flash, redirect, url_for,render_template

from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.view_models.gift import MyGifts
from . import web


@web.route('/my/gifts')
@login_required
def my_gifts():
    '''
    赠送清单: 将赠送清单gift要保存的信息保存
            1 用户id
            2 礼物数据(赠送的书籍列表)
            3 心愿数据(想要获取人数)
    :return:
    '''
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gift(uid)
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_count(isbn_list)
    view_model = MyGifts(gifts_of_mine,wish_count_list)
    return render_template('my_gifts.html',gifts=view_model.gifts)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    '''
    保存到赠送清单  1 确定是否能保存到清单
                2 礼物的isbn  用户id  鱼漂数量增加
    :param isbn:
    :return:
    '''
    if current_user.can_save_to_list(isbn):
        '''
        事务 回滚机制
        一般只要进行db.session.commit()
        最好try..except..进行事务的回滚操作
        '''
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
    else:
        flash('这本书已经添加至您的赠送清单或已存在您的心愿清单,不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    '''
    赠送清单中撤销操作: 1 查询所有礼物 鱼漂
                    2 礼物状态修改  鱼漂数值撤销
    :param gid:
    :return:
    '''
    gift = Gift.query.filter_by(id=gid,launched=False).first()
    if not gift:
        flash('该书籍不存在,或已经处于交易状态,撤销失败!')
    drift = Drift.query.filter_by(gift_id=gid,pending=PendingStatus.Waiting).first()
    if drift:
        flash('这个礼物正处于交易状态,请先在鱼漂出完成交易!')
    else:
        with db.auto_commit():
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
            gift.delete()
    return redirect(url_for('web.my_gifts'))
