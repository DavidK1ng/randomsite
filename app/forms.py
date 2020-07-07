from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired(message='Please type in your user name')])
    password = PasswordField('Password', validators=[DataRequired(message='Please type in your password')])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')