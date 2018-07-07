from flask import Blueprint,render_template

'''蓝图 blueprint '''
web = Blueprint('web',__name__)  #__name__代表蓝图所在模块


@web.app_errorhandler(404)
def not_found(e):
    '''
    AOP: 处理所有的404请求
    '''
    return render_template('404.html'),404

@web.app_errorhandler(500)
def internal_server_error(e):
    '''
    AOP: 处理所有的500请求
    '''
    return render_template('500.html'),500


from app.web import book  #在此处导入代表先初始化在导入应用
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish