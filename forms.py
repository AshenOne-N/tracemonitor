from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField,BooleanField
from wtforms.validators import DataRequired, Length


class SignUpForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired(), Length(1, 20)])
    ID = StringField('学号', validators=[DataRequired(), Length(1, 200)])
    submit = SubmitField('提交')


class LoginForm(FlaskForm):
    name = StringField('账号', validators=[DataRequired(), Length(1, 20)])
    pswd = PasswordField('密码',validators=[DataRequired(),Length(6,8)])
    remember = BooleanField('记住我')
    submit = SubmitField('提交')