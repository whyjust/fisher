from threading import Thread

from app import mail
from flask import current_app,render_template
from flask_mail import Message

'''开启异步线程'''
def send_async_mail(app,msg):
    '''mail.send发送需要获取上下文,因此添加with'''
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            raise e


def send_mail(to, subject, template,**kwargs):
    '''
    发送邮件
    :param to: 收件人
    :param subject: 标题
    :param template: 渲染模板
    :param kwargs: 关键字参数
    :return:
    '''
    msg = Message('[鱼书]'+ '' +subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template,**kwargs)
    '''
    current_app是代理对象,开启新的线程时,我们直接获取真实的app核心对象_get_current_object()
    '''
    app = current_app._get_current_object()
    thr = Thread(target=send_async_mail,args=[app,msg])
    thr.start()

