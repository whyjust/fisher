## 鱼书学习(一)

**1 安装环境**

```python
python -V  #查看版本
pip -V     #查看版本
pip list   #查看列表

makedir fisher      #新建项目目录
pip install pipenv  #进入项目目录安装pipenv

pipenv install   #创建的虚拟环境绑定到项目目录
pipenv shell     #激活项目,启动虚拟环境
```

**2 安装flask**

```python
pipenv install flask   #用pipenv安装flask
pipenv graph           #查看flask版本与依赖
pipenv --venv          #查看当前的虚拟环境解释器路径（在pycharm中设置）

pipenv install -r requirements.txt    #通过requirements.txt安装包
pipenv lock -r --dev > requirements.txt  #像virtualenv一样用命令生成requirements 文件

pipenv shell    激活虚拟环境
python fisher.py    启动服务
```

**3 工具**

```python
常用命令
 1 pipenv --where               列出本地工程路径
 2 pipenv --venv                列出虚拟环境路径
 3 pipenv --py                  列出虚拟环境的Python可执行文件
 4 pipenv install               安装包（创建虚拟环境）
 5 pipenv install moduel --dev  在开发环境安装包
 6 pipenv graph                 查看包依赖
 7 pipenv lock                  生成lockfile
 8 pipenv install --dev         安装所有开发环境包
 9 pipenv uninstall --all       卸载所有包
10 pipenv --rm                  删除虚拟环境

Pycharm (vs code)
Xampp (mysql)
Navicat(数据化可视化工具)

#启动虚拟环境
方法一： 
pipenv run python xxx.py
方法二：启动虚拟环境的shell环境
pipenv shell
python xxx.py 
```

**4 flask注意事项**

```python
1 @app.route('/hello/')  #原理是进行了重定向，按照 /hello输入  服务器进行了两个过程
hello   服务器返回状态码301 并设置location重定向 127.0.0.1：5000/hello/，并再次返回200状态码 

2 app.add_url_rule('/hello',view_func=hello)
装饰器@app.route('/hello/')其实就是装饰器函数调用app.add_url_rule('/hello',view_func=hello)方法
如果使用基于类的视图(即插视图),只能通过app.add_url_rule('/hello',view_func=hello)

3 host如果想外网访问: host=0.0.0.0,端口port也可以设置

4 配置文件的加载与导入
app.config.from_object('config')
app.config['DEBUG']  #config类本身就是dict的子类,因此可以字典形式访问

5 DEBUG是默认python中的默认参数为DEBUG=False,config['DEBUG']没找到DEBUG则默认False
  找到config['DEBUG']则覆盖掉
```

**5 简化if else**

```python
r = requests.get(url)
r.json() if return_json else r.text  
#三元表达式   [真返回  if 条件 else 假执行]  先输出r.json() 如果return_json为假输出r.text
```

**6 类方法 静态方法**

```python
@classmethod  #类方法,当参数需要类不需要实例对象使用
def search_by_keyword(cls,keyword,page=1):
   url = cls.keyword_url.format(keyword,current_app.config['PER_PAGE'],cls.calulate_start(page))
   result = Http.get(url)
   return result

@staticmethod  #当方法中既不需要cls类,也不需要实例对象使用
def calulate_start(page):
    return (page-1)* current_app.config['PER_PAGE']
```

**7 API接口**

```python
API难点不在于编写返回的数据,而在于对路由的设计定位
API实质就是提供的数据接口
 
#API+JS  前后端分离  SEO
#网站多页面ajax

#dict序列化 返回为元组,这就是API接口
return jsonify(result)  #flask中提供了jsonify,效果一致
return json.dumps(result),200,{'content-type':'application/json'}   #python中写法
```

**8 一般常见app下的目录结构与框架搭建**

```python
#app应用
	cms  #文件存放
    form  #表单类或表单验证
    	book.py  #书相关验证
    libs  #自定义类及帮助文档
    	helpper.py
        httper.py
    models
    	book.py  #模型类
    web   #蓝图web
    	__init__.py
    	book.py
        user.py    
    spider  #持久化存储
    	__init__.py
    secure.py   #秘钥安全验证之类的配置
    setting.py  #生产测试通用的配置
fisher.py

#fisher.py
from app import create_app
app = create_app()
if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])

#app.__init__.py
from flask import Flask
from app.models.book import db

def create_app():
    '''
    系统配置注册与蓝图需要绑定app
    '''
    app = Flask(__name__)
    app.config.from_object('app.secure')  #系统配置
    app.config.from_object('app.setting') #系统配置
    register_blueprint(app)
	'''初始化数据库'''
    db.init_app(app)
    db.create_all(app=app)
    return app

def register_blueprint(app):
    '''蓝图注册'''
#视图函数   帮助文档   模型类   表单类    数据API统一接口
```

**9 数据表创建三种方式**

```python
# database first   通过建表工具直接创建
# module first  通过创建模型生成数据表结构
# code first  通过ORM映射来生成数据表结构

flask在sqlalchemy 中封装了Flask_SQLAlchemy
flask在WTFORMS 中封装了Flask_WTFORMS

from sqlalchemy import Column,Integer,String  #通过sqlalchemy导入基本数据类型
from flask_sqlalchemy import SQLAlchemy  #通过flask_sqlalchemy导入SQLAlchemy核心对象

secure中配置
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:20111673@111.230.169.107:3306/fisher'
#方法1:
def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    db.init_app(app)
    db.create_all(app=app)  #关键字传递app核心对象
    return app
#方法二:
def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    db.init_app(app)
    with app.app_context(): #with上下文管理app核心对象
    	db.create_all()
    return app
#方法三
db = SQLAlchemy(app=app)

```

**10 flask中上下文**

```python
应用级别上下文    对象 Flask封装
请求级别上下文    对象 Request封装
Flask核心对象     存储在Flask  AppContext
Request请求对象   存储在Request  RequestContent
让需要获取的两种对象时,我们往往不是通过直接导入获取,而是通过localproxy本地代理间接获取

from flask import Flask,current_app

#入栈方法一:
app = Flask(__name__)     #获取app核心对象
ctx = app.app_context()   #获取应用上下文
ctx.push()                #将应用上下文入栈
a = current_app.config['DEBUG']  #返回的current_app是指应用上下文的app属性
ctx.pop()   #出栈

#应用上下文源码:
current_app = LocalProxy(_find_app)  #返回的是app
def _find_app():
    top = _app_ctx_stack.top
    if top is None:
        raise RuntimeError(_app_ctx_err_msg)
    return top.app

#请求上下文源码:
request = LocalProxy(partial(_lookup_req_object, 'request'))
def _lookup_req_object(name):
    top = _request_ctx_stack.top
    if top is None:
        raise RuntimeError(_request_ctx_err_msg)
    return getattr(top, name)  #返回的是request对应的属性

# with: 可以对实现了上下文协议的对象使用with,对资源进行连接,操作及关闭,例如:数据库与文件读写操作
# 上下文管理器: 实现了__enter__与__exit__两个方法
# 上下文表达式必须返回一个上下文管理器
with app.app_context():
    a = current_App.config['DEBUG']

class A: #上下文管理器
    def __enter__(self): #代表进入上下文环境
        a = 1
        return a
    def __exit__(self): #代表退出上下文环境
        b = 2
with A() as obj_A: #obj_A返回的是__enter__放下对应的值a=1
    pass
```

![img](http://images.cnblogs.com/cnblogs_com/why957/1223614/o_flask%e4%b8%8a%e4%b8%8b%e6%96%87%e8%af%a6%e8%a7%a3.png)

**11 线程与进程**

```python
进程: 计算机竞争资源的最小单位,占用cpu资源进程,更多是用来分配管理资源. 各个进程根据调度算法实现进程的切	换,明显的缺点是切换开销大,因此进程切换肯定要被淘汰,比进程小的单元线程的诞生!
线程: 进程的一部分,一个进程包含至少一个线程,线程更多是用来执行访问资源的,不占用CPU资源,线程的工作是用过	访问进程cpu资源进行的,由于是在进程内部切换,因此开销明显小很多!

#GIL  全局线程锁 
线程是不占有资源,需要访问进程内部的资源的,因此共享资源就会产生一个资源的冲突.因此锁机制就是保证同一时刻只允许一个线程进行访问.
细粒度锁  程序员  主动加锁
粗粒度锁  解释器  GIL

CPU密集型程序  进行CPU密集计算,例如视频的解码操作
IO密集型程序   查询数据库 请求网络资源 读写文件

#flask线程隔离  原因:一个变量对应多个对象引用时,存在引用混乱  原理  字典  保存数据  
通过werkzeug库  local模块   Local对象字典管理(获取id号与键值对对应{19943,{key:value}})
使用线程隔离的意义在于使用当前线程能正确地引导到自己所创建的对象,而不是引用到其他线程创建的对象

#LocalStack  Local   字典的三者区别
Local通过字典的方式实现线程隔离
LocalStack通过封装Local对象并将其作为私有属性,实现线程隔离的栈结构

s = LocalStack()  #栈结构  先进后出
s.push(1)
s.push(2)
print(s.top)  #2
print(s.top)  #2
print(s.pop())  #2
print(s.top)  #1

#以线程ID号作为key的字典 ->Local ->LocalStack
#AppContext RequestContext -> LocalStack
#Flask -> AppContext  Request -> RequestContext
#current_app -> (LocalStack.top=AppContext  top.app=flask) 栈顶取出上下文,app核心对象是上下文的属性
#request -> (LocalStack.top=RequestContext top.request=Request)  指向Request请求对象
```

```python
#local隔离
import time
from werkzeug.local import Local

class A:
    b = 1
my_obj = Local()  #将my_obj进行隔离

def worker():
    my_obj.b = 2
    print(my_obj.b)  #输出2
    
new_th = threading.Thread(target=worker,name='one_thread')
new_th.start()
time.sleep(1)
print(my_obj.b)  #输出1

#LocalStack线程隔离
from werkzeug.local import LocalStack

my_stack = LocalStack()
my_stack.push(1)
print('in main thread after push,value is' + str(my_stack.top))  #1

def worker():
    print('in new thread after push,value is' + str(my_stack.top))  #None
    my_stack.push(2)
    print('in new thread after push,value is' + str(my_stack.top))  #2
new_t = threading.Thread(target=worker,name='ne_thread')
new_th.start()
time.sleep(1)

print('finally,in main thread after push,value is' + str(my_stack.top))  #1
```

#### 12  编程思维 

```python
	后端数据应该在原始数据的基础上进行统一格式的模块封装,用户查询的方式可能不同,但是我们返回的数据结构类型应该保持统一格式,提供便捷的API接口

面向对象编程应该包含:
	特征(类变量,实例变量) 
	行为(方法)

#类的重构: 首先要明白类的具体定位,具体作用,为什么要面向对象编程
class YuShuBook:
    '''
    模型层: mvc中 M层
    '''
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    @classmethod
    def search_by_isbn(cls,isbn):
        url = cls.isbn_url.format(isbn) #或者self.isbn_url.format(isbn)
        result = Http.get(url)  #dict
        return result

    @classmethod
    def search_by_keyword(cls,keyword,page=1):
        url = cls.keyword_url.format(keyword,current_app.config.get('PER_PAGE'),
                                     cls.calulate_start(page))
        result = Http.get(url)
        return result

    @staticmethod
    def calulate_start(page):
        return (page-1)* current_app.config.get('PER_PAGE')

#view_models.book.py
class BookViewModel:
    #对原始数据进行数据格式统一(裁切,合并等操作)
    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls.__cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = data['total']
            returned['books'] = [cls.__cut_book_data(book) for book in data['books']]
        return returned

    @classmethod
    def __cut_book_data(cls, data):
        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'pages': data['pages'],
            'author': '、'.join(data['author']),
            'price': data['price'],
            'summary': data['summary'],
            'image': data['image']
        }
        return book

    
#类的重构之后区别:类不但定义了方法,而且重构后具有过滤保存精准查询信息的功能
from flask import current_app
from app.libs.httper import Http

class YuShuBook:
    '''
    模型层: mvc中 M层
    '''
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    keyword_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'
    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self,isbn):
        url = self.isbn_url.format(isbn) #或者self.isbn_url.format(isbn)
        result = Http.get(url)  #dict
        self.__fill_single(result)

    def search_by_keyword(self,keyword,page=1):
        url = self.keyword_url.format(keyword,current_app.config.get('PER_PAGE'),
                                      self.calulate_start(page))
        result = Http.get(url)
        self.__fill_collection(result)

    def __fill_single(self,data):
        if data:
            self.total = 1
            self.books.append(data)

    def __fill_collection(self,data):
        if data:
            self.total = data['total']
            self.books = data['books']

    def calulate_start(self,page):
        return (page-1)* current_app.config.get('PER_PAGE')
 
#view_models.book.py  
class BookViewModel:
    def __init__(self,book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.author = book['author']
        self.image = book['image']
        self.price = book['price']
        self.summary = book['summary']
        self.pages = book['pages']

class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self,yushu_book,keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]
```

#### 13 序列化与反序列化

```python
json.dumps(s, default=lambda obj: obj.__dict__)序列化 (serialization)

序列化是将对象状态转换为可保持或传输的格式的过程。与序列化相对的是反序列化，
它将流转换为对象。这两个过程结合起来，可以轻松地存储和传输数据。

序列化和反序列化的目的　　
1、以某种存储形式使自定义对象持久化；　　
2、将对象从一个地方传递到另一个地方。　　
3、使程序更具维护性

(1)python提供了pickle

pickle.dumps(obj)  方法把任意对象序列化成一个bytes，然后，就可以把这个bytes写入文件
import pickle
d = dict(name='Bob', age=20, score=88)
pickle.dumps(d)
b'\x80\x03}q\x00(X\x03\x00\x00\x00ageq\x01K\x14X\x05\x00\x00\x00scoreq\x02KXX\x04\x00\x00\x00nameq\x03X\x03\x00\x00\x00Bobq\x04u.'

当我们要把对象从磁盘读到内存时，可以先把内容读到一个bytes，然后用pickle.loads()方法反序列化出对象

(2)更方便的是采用python中json库的做法
def dumps(obj, *, skipkeys=False, ensure_ascii=True, check_circular=True,
        allow_nan=True, cls=None, indent=None, separators=None,
        default=None, sort_keys=False, **kw):

json.dumps(dict)接受一个必须参数（如dict），结果是str
json.dump()接受两个必须参数，第一个如dict，第二个是类文件名
json.dumps()和dump序列化对象时用 default=lambda obj: obj.dict

def load(fp, *, cls=None, object_hook=None, parse_float=None,
        parse_int=None, parse_constant=None, object_pairs_hook=None, **kw):
json.loads()接受一个必需参数，把json变为如dict，
json.load()接受一个必需参数（类文件名），把类文件中的json变为如dict
json.loads()和load反序列化json（对象）时需要object_hook=参数

>>> import json
>>> d = dict(name='Bob', age=20, score=88)
>>> json.dumps(d)
'{"age": 20, "score": 88, "name": "Bob"}'

>>> json_str = '{"age": 20, "score": 88, "name": "Bob"}'
>>> json.loads(json_str)
{'age': 20, 'score': 88, 'name': 'Bob'}


(3) 问题来了,json可以很方便的完成字典与json的转换,但是python中更多的是类与实例对象,那么如何来定制json
json存在一个可选参数default
可选参数default就是把任意一个对象变成一个可序列为JSON的对象，我们只需要为Student专门写一个转换函数

通常class的实例都有一个__dict__属性，它就是一个dict，用来存储实例变量:obj.__dict__可以转字典格式
因此: 
	json.dumps(s, default=lambda obj: obj.__dict__) #实现对象与字典的转换

那么,反序列化类似:
json_str = '{"age": 20, "score": 88, "name": "Bob"}'
def dict2student(d):
    return Student(d['name'], d['age'], d['score'])
print(json.loads(json_str, object_hook=dict2student))

#输出为对象:<__main__.Student object at 0x10cd3c190>    
```

#### 14 高阶函数

一般我们也会与lambda函数配合,非常方便的取代if判断效果.

```python
class BookViewModel:
    self.publisher = book['publisher']
    self.author = book['author']
    self.price = book['price']
    
def intro(self):
        intros = filter(lambda x:True if x else False,[self.author,self.publisher,self.price])
        return '/'.join(str(s) for s in intros)
```

`lambda x:True if x else False`可以实现对x是否为空的判定,X存在返回True,并保留,X不存在返回空并排除.

> > 注意: 
> >
> > join函数组合可迭代对象时,当对象中存在数字与字符串类型不同时,需要转成统一格式再组合.一般采		    取的做法是先遍历可迭代对象转统一格式后合并.  `'/'.join(str(s) for s in intros)`

#### **15 flask路由**

对于需要校验的路由,一般在form下面新建一个表单类,由表单类完成校验
对于需要处理 GET 与 POST两种不同的请求,一般在视图函数中添加methods

```python
#注册时候表单类验证
class RegisterForm(Form):
    email = StringField(validators=[DataRequired(),Length(8,64),Email(message='电子邮箱不合规范')])
    password = PasswordField(validators=[DataRequired(message='密码不能为空')])
    nickname = StringField(validators=[DataRequired(),Length(2,10,message='昵称至少需要两个字符,最多10个字符')])

#可以同时处理GET与POST请求
@web.route('/register', methods=['GET', 'POST'])
```

#### 16 flask密码存储与setattr  hasattr  getattr 与property

```python
#在User类下面对一些特殊的验证操作单独验证
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw):
        self._password = generate_password_hash(raw)

    def check_password(self,raw):
        return check_password_hash(self._password,raw)
    
 #注册
@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User()
        user.set_attrs(form.data)
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        redirect(url_for('web.login'))
    return render_template('auth/register.html',form=form)

#登录
@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user,remember=True)
        else:
            flash('账号不存在或者密码错误')
    return render_template('auth/login.html',form=form)
```

登录注册flask_login用户管理模块的使用

`app.__init__.py`

```python
from flask_login import LoginManager

login_manager = LoginManager()
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
    db.create_all(app=app)
    login_manager.init_app(app)
    login_manager.login_view = 'web.login' #重定向视图函数为login
    login_manager.login_message = '请先登录或者注册'
    return app
```

`models.user.py`

```python
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

from app.models.base import Base
from sqlalchemy import Column, Integer, String, Boolean, Float
from app import login_manager


class User(Base,UserMixin):

    '''
    模型属性设置
    '''
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    _password = Column('password',String(128),nullable=True)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
	...
    
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,raw):
        self._password = generate_password_hash(raw)

    def check_password(self,raw):
        return check_password_hash(self._password,raw)

'''用户的回调'''
@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
# 这个callback函数用于reload User object，根据session中存储的user id
```

flask_login的权限分级

通过装饰器来实现不同用户组,不同的视图函数访问权限

flask_login封装了关于用户信息的内容,当然也可以根据需求自己定义不同权限的装饰器,比如会员,管理员等等

```python
from flask_login import login_required,current_user
```

#### 17  contextmanager模块的使用

我们通常用with管理上下文,一般上下文管理器

```python

class MyResource:
    def __enter__(self):
        print('connect to resource')
        return self
    def __exit__(self,exc_type,exc_value,tb):
        print('close resource connection')
    def query(self):
        print('query data')
 with MyResource() as r:
    r.query()

#输出
connect to resource
query data
close resource connection
```

那么采用`contextmanager`的管理器做法

```python
from contextlib import contextmanager
@contextmanager
def make_myresource():
    print('connect to resource')
    yield MyResource()
	print('close resource connection')

@contextmanager
def make_myresource():
    print('connect to resource')
    yield MyResource()
    print('close resource connection')
with make_myresource() as r:
    r.query()
    
#输出
connect to resource
query data
close resource connection
```

可以发现用`@contextmanager`装饰过的函数具备上下文管理器功能,然后可以通过with进行资源管理,此处yield作用是生成器,保存执行完`yield MyResource()`,后续代码`print('close resource connection')`继续执行.

那么实际代码中我们用到地方

`base.py`

```python
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from sqlalchemy import Column, Integer, SmallInteger
from contextlib import contextmanager

#实例化数据库时我们可以通过 继承+自定义上下文管理 实现自动提交回滚 提高代码复用度
class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
db = SQLAlchemy()

class Base(db.Model):
    '''
    该模型表不想在数据库创建
    '''
    __abstract__ = True
    creat_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

```

`gift.py`

```python
@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        '''
        事务 回滚机制
        一般只要进行db.session.commit()
        最好try..except..进行事务的回滚操作 
        '''
        # try:
        with db.auto_commit():
            '''
            通过调用自定义auto_commit()管理器实现数据的提交与自动回滚操作
            '''
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
            # db.session.commit()
            # except Exception as e:
            #     db.session.rollback()
            #     raise e
    else:
        flash('这本书已经添加至您的赠送清单或已存在您的心愿清单,不要重复添加')
```

如果是在同一个页面的局部刷新,或者需求是不需要跳转,我们应该尽量采用`ajax` 与 页面缓存的方式尽量减少服务器压力 , 实现`ajax `在`js`中实现 

**18 登录验证与多表查询**

多表关联查询

```python
#判断是否登录
if current_user.is_authenticated:
    #多表查询
    if Gift.query.filter_by(uid=current_user.id,isbn=isbn,launched=False).first():
        has_in_gifts = True
    if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first():
        has_in_wishes = True
#所有赠送者信息
trade_gifts = Gift.query.filter_by(isbn=isbn,launched=False).all()
#所有索要者清单
trade_wishes = Wish.query.filter_by(isbn=isbn,launched=False).all()
trade_wishes_model = TradeInfo(trade_wishes)
trade_gifts_model = TradeInfo(trade_gifts)
```

view_models中定义trade数据裁切

```python
class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self, single):
        if single.create_datetime:
            time = single.create_datetime.strftime('%Y-%m-%d')
        else:
            time = '位置'
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id
        )
```

重写基类的方法filter_by

```python
class Query(BaseQuery):
    '''
    自定义基类(继承,初始化),重写filter_by方法
    '''
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query,self).filter_by(**kwargs)

db = SQLAlchemy(query_class=Query)  #传递一对关键字参数query_class=Query
```

数据库数据的链式调用

```python
class Gift(Base):
    '''
    gift通过relationship关联到User模型类
    并通过userid外键关联到gift
    '''
    id = Column(Integer, primary_key=True)
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    isbn = Column(String(15), nullable=False)
    launched = Column(Boolean, default=False)
    @classmethod
    def recent(cls):
            #链式调用
            #主体query
            #子函数
            #触发函数
            recent_gift = Gift.query.filter_by(launched=False).group_by().order_by(Gift.create_time).limit(current_app.config['RECENT_BOOK_COUNT']).distinct().all()
        return recent_gift
```

转成对象方法的原因是:

最近接受的礼物存在多个礼物,如果参数为self代表具体的实例即一个礼物

转成类方法之后参数为抽象的类,可以代表所有的礼物

#### 19 循环导入问题

出现循环导入主要问题是类还没被执行就导入,因此解决办法是将相互导入的两个模块类分别放在模块的最后导入.

```python
#wish.py
class Wish(object):
    pass
from app.models.gift import Gift

#gift.py
class Gift(object)
	pass
from app.models.wish import Wish
```

当然也可以针对在哪调用 , 可以在哪导入`from app.models.wish import Wish` 可以写在函数内部导入.

#### 20 python可调用对象

python中常见的可调用对象是  函数, 方法, 类及类的实例

函数一般分为三种: 

内建函数 : 在`_builtin_`模块里

```python
>>> dir(type)
['__abstractmethods__', '__base__', '__bases__', '__basicsize__', '__call__', '__class__', '__delattr__', '__dict__', '__dictoffset__', '__doc__', '__eq__', '__flags__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__instancecheck__', '__itemsize__', '__le__', '__lt__', '__module__', '__mro__', '__name__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasscheck__', '__subclasses__', '__subclasshook__', '__weakrefoffset__', 'mro']
```

自定义函数

```python
>>> type(foo)
<type 'function'>
```

lambda表达式

```python
>>> lambdaFunc = lambda x: x * 2
>>> lambdaFunc(12)
24
>>> type(lambdaFunc)
<type 'function'>
>>> lambdaFunc.__name__
'<lambda>'
```

封装的类如果想作为参数传递调用 , 必须添加`__call__`方法 , 调用类的结果就是创建了实例，也就是实例化。

Python给类提供了名为`__call__`的特别方法，该方法允许程序员创建可调用的对象(实例)。默认情况下，`__call__()`方法是没有实现的，这意味着大多数情况下实例是不可调用的。然而，如果在类中覆盖了这个方法，那么这个类的实例就成为可调用的了。调用这样的实例对象等同于调用`__call__`()方法。如：`foo()`和`foo.__call__(foo)`的效果相同，这里的foo也作为参数出现，因为是对自己的引用，实例将自动成为每次方法调用的第一个参数，如果`__call__()`有参数，那么`foo(arg)`就和`foo.__call__(foo, arg)`一样。

**可调用对象的作用:**

1. 简化对象的方法的调用

   (1)`a.func()`  实例调用方法

   通过将func()写入`__call__`可以实现 `a()` 直接调用该方法

   (2) 类下面有很多方法,但是只有一个常用,其他的都不是很常用

   这种情况我们可以将常用的方法写在`__call__`函数下

2. 模糊对象与函数的区别: 统一调用接口

   ```python
   #通过__call__可调用对象实现A()/b()直接调用__call__方法下的返回值
   class A():
       def __call__(self):
           return object()
   class B():
       def __call__(self):
           return object()
   def main(callable):
       callable()
   ```

#### 21 flask中异常的捕获

当我们有异常状态码,异常的页面渲染的需求时,我们可以主要采用flask封装的模块,AOP编程的思想

抛出异常状态码: flask封装好的  自定义抛出的

下面以404页面为例:

```python
first_or_404()	返回查询的第一个结果，如果没有结果，终止请求，返回 404 响应错误
get_or_404()	返回指定主键对应的行，如果没有指定的主键，终止请求，返回 404 响应错误

abort = 404  自己抛出
```

flask 实现的404状态码的捕获操作

```python
'''监控所有的404状态码的抛出'''
@web.app_errorhandler(404)
def not_found(e):
    return render_template('404.html'),404
```

#### 22 发送邮件及忘记密码的封装

`mail.py`模块

```python
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

'''
发送邮件
'''
def send_mail(to, subject, template,**kwargs):
    msg = Message('[鱼书]'+ '' +subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template,**kwargs)
    '''
    current_app是代理对象,开启新的线程时,我们直接获取真实的app核心对象
    '''
    app = current_app._get_current_object()
    thr = Thread(target=send_async_mail,args=[app,msg])
    thr.start()
```

`auth.py`模块中

```python
@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
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
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token,form.password1.data)
        if success:
            flash('您的密码重置成功')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html')
```

`user.py`模块中

```python
from itsdangerous import  TimedJSONWebSignatureSerializer as Serializer
class user:
    ...
    
    '''生成用户id信息的token,添加到get请求中标识身份'''
    def generate_token(self, expiration=600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'id':self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token,new_password):
        '''解压出用户id信息,并根据ID查询相关的内容'''
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            if user:
                user.password = new_password
        return True
```

#### 23 模型设计

模型存在关联

>优点 : 每次查询的信息都是最新的,避免重复存数据库

>缺点: 不能真实的反映记录交易时的状态(其他表信息发生更改时,相应发生变更)

模型无关联时

>优点 : 减少查询次数,数据存储后不随其他表更改

>缺点 : 数据有冗余,重复存储(合理利用即可)

