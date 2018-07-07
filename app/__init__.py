'''创建flask核心对象'''
from flask import Flask
from app.models.base import db
from flask_login import LoginManager
from flask_mail import Mail
from app.libs.limiter import Limiter


login_manager = LoginManager()
mail = Mail()
limiter = Limiter()


def create_app():
    '''
    系统配置与蓝图需要绑定app
    :return:
    '''
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或者注册'

    mail.init_app(app)
    with app.app_context():
        db.create_all()
    return app


def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)
