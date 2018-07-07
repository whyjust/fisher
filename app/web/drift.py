from flask import flash, redirect, url_for, render_template, request,current_app
from sqlalchemy import desc, or_

from app.form.book import DriftForm
from app.libs.email import send_mail
from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.book import BookViewModel
from app.view_models.drift import DriftCollection
from . import web
from flask_login import login_required, current_user


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    '''
    向他人请求此书  1 判断能否请求
                2 判断书籍的id 与 归属
                3 请求的详情页面
                4 发送邮件申请
    :param gid:
    :return:
    '''
    current_gift = Gift.query.get_or_404(gid)
    if current_gift.is_yourself_gift(current_user.id):
        flash('这本书属于你,不能向自己所要哦!!')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))
    else:
        can = current_user.can_send_drift()
        if not can:
            return render_template('not_enough_beans.html', beans=current_user.beans)
        form = DriftForm(request.form)
        if request.method == 'POST' and form.validate():
            save_drift(form, current_gift)
            send_mail(current_gift.user.email, '有人想要一本书', 'email/get_gift.html',
                      wisher=current_user,
                      gift=current_gift)
            return redirect(url_for('web.pending'))
        gifter = current_gift.user.summary
        return render_template('drift.html', gifter=gifter, user_beans=current_user.beans, form=form)


@web.route('/pending')
@login_required
def pending():
    '''
    鱼漂的交易状态: 展示列表信息
    '''
    drifts = Drift.query.filter(
        or_(Drift.request_id == current_user.id,
            Drift.gifter_id == current_user.id)).order_by(desc(Drift.create_time)).all()
    views = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=views.data)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    '''
    拒绝操作 : 只有确定书籍赠送者才能拒绝请求
    注意超权
    '''
    with db.auto_commit():
        drift = Drift.query.filter(Gift.uid==current_user.id,
                                   Drift.id==did).first_or_404()
        drift.pending = PendingStatus.Reject
        db.session.add(drift)
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    '''
    撤销操作:存在超权
    uid  :1  did:1
    uid  :2  did:2
    '''
    with db.auto_commit():
        drift = Drift.query.filter_by(
            id=did,request_id=current_user.id).first_or_404()
        drift.pending = PendingStatus.Redraw
        current_user.beans += 1
        db.session.add(drift)
    return redirect(url_for('web.pending'))

@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    '''
    邮寄操作 :  只有书籍的赠送者才可以确认邮寄
    '''
    with db.auto_commit():
        drift = Drift.query.filter_by(gifter_id=current_user.id,
                                   id=did).first_or_404()
        drift.pending = PendingStatus.Success
        current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
        gift = Gift.query.filter_by(id=Drift.gift_id).first_or_404()
        gift.launched = True

        #不查询直接更新
        Wish.query.filter_by(isbn=drift.isbn,uid=drift.request_id,
                             launched=False).update({Wish.launched:True})
    return redirect(url_for('web.pending'))

def save_drift(drift_form, current_gift):
    '''
    保存  鱼漂模型
    实现将DriftForm表单中的信息赋值到drift模型中
    :param drift_form:
    :param current_gift:
    :return:
    '''
    with db.auto_commit():
        drift = Drift()
        '''快速实现复制'''
        drift_form.populate_obj(drift)
        '''请求者信息'''
        drift.gift_id = current_gift.id
        drift.request_id = current_user.id
        drift.request_nickname = current_user.nickname
        '''赠送者信息'''
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id
        '''书籍类信息'''
        book = BookViewModel(current_gift.book)
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn

        current_user.beans -= 1
        db.session.add(drift)
