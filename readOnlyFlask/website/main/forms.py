from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length

class HindiInputForm(FlaskForm):
    pastInput=TextAreaField('Input Hindi Text Here', validators=[DataRequired()])
    submit=SubmitField('Submit')
