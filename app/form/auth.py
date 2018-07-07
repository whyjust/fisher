from wtforms import Form,StringField,PasswordField
from wtforms.validators import Length,DataRequired,Email, ValidationError,EqualTo

from app.models.user import User


class RegisterForm(Form):
    '''表单验证'''
    email = StringField(validators=[DataRequired(),Length(8,64),Email(message='电子邮箱不合规范')])
    password = PasswordField(validators=[DataRequired(message='密码不能为空')])
    nickname = StringField(validators=[DataRequired(),Length(2,10,message='昵称至少需要两个字符,最多10个字符')])

    '''自定义验证器'''
    def validate_email(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self,field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已经存在')


class LoginForm(Form):
    '''
    登录表单验证
    '''
    email = StringField(validators=[DataRequired(),Length(8,64),Email(message='电子邮箱不合规范')])
    password = PasswordField(validators=[DataRequired(message='密码不能为空')])


class EmailForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不合规范')])


class ResetPasswordForm(Form):
    password1 = PasswordField(validators=[
        DataRequired(),Length(6,32,message='密码长度至少需要6-32字符之间'),
        EqualTo('password2',message='两次输入的密码不一致')])
    password2 = PasswordField(validators=[
        DataRequired(),Length(6,32)])


class ChangePasswordForm(Form):
    old_password = PasswordField('原有密码',validators=[DataRequired()])
    new_password1 = PasswordField('新密码', validators=[DataRequired(), Length(6, 10, message='密码长度至少需要在6到20个字符之间'),EqualTo('new_password2', message='两次输入的密码不一致')])
    new_password2 = PasswordField('确认新密码字段', validators=[DataRequired()])