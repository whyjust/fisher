'''
配置文件:保存单独的加密信息,secure不要上传git
'''
DEBUG = True

# 单数据库
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:xxx@xxx:3306/fisher'

SECRET_KEY = '\SAAFsdfsdf:sdadzxcsd,./.dasdafasd'

#Email相关配置
MAIL_SERVER = 'smtp.163.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = 'xxx.@163.com'
MAIL_PASSWORD = 'xxx'
