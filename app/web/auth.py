from app.libs.email import send_mail
from app.models.base import db
from app.models.user import User
from . import web
from flask import render_template, request, redirect, url_for, flash
from app.form.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm,ChangePasswordForm
from flask_login import login_user,logout_user,current_user,login_required

@web.route('/register', methods=['GET', 'POST'])
def register():
    '''
    注册  1 表单验证+POST
        2 提交用户信息
    :return:
    '''
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            user.password = form.password.data
            db.session.add(user)
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)

@web.route('/login', methods=['GET', 'POST'])
def login():
    '''
    登录  1 表单验证+POST
        2 验证用户名与密码
        3 一些未登录操作做好相关记录重定向
    :return:
    '''
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # login_user(user,remember=True) 可以加入记忆
            login_user(user)
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号不存在或者密码错误')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    '''
    忘记密码: 发起忘记密码请求,发送邮件
    :return:
    '''
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            user = User.query.filter_by(email=account_email).first_or_404()
            send_mail(form.email.data,'重置您的密码','email/reset_password.html',user=user,
                      token=user.generate_token())
            flash('一封邮件已经发送到邮箱'+account_email+',请及时查收!')

    return render_template('auth/forget_password_request.html',form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    '''
    忘记密码: 1 需要POST验证表单验证
            2 邮箱链接需要传递 id 因此采用携带token表名身份
    :param token:
    :return:
    '''
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token,form.password1.data)
        if success:
            flash('您的密码重置成功')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html')

@web.route('/change/password', methods=['GET', 'POST'])
@login_required
def change_password():
    '''
    修改密码:  1 此处特别注意表单类的名字与渲染页面form表单name一致
            2 直接访问password 设置即可
    :return:
    '''
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        current_user.password = form.new_password1.data
        db.session.commit()
        flash('密码更新成功!!')
        return redirect(url_for('web.index'))
    return render_template('auth/change_password.html',form=form)

@web.route('/logout')
@login_required
def logout():
    '''
    注销: 调用logout_user即可
    :return:
    '''
    logout_user()
    return redirect(url_for('web.index'))

