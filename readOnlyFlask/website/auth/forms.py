from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User
from email_validator import validate_email

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email=StringField('Email:', validators=[DataRequired(), Length(1, 64),Email()])
    password=PasswordField('Enter password:', validators=[DataRequired(), Length(8,64)])
    remember_me=BooleanField('Remember Me')
    submit=SubmitField('Submit')


def check_email_already_registered(field):
    if User.query.filter_by(email=field.data).first():
        raise ValidationError('Email already registered.')


