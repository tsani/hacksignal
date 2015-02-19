from app import app
from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, TextAreaField
from wtforms.validators import Email, Length, DataRequired, NumberRange

class MentorRequestForm(Form):
    user_name = StringField('Full name', validators=[
        DataRequired(), Length(max=50)])
    user_email = StringField('Email address', validators=[
        DataRequired(), Length(max=255), Email()])
    ticket_contents = TextAreaField("What's up? (max. 150 chars)", validators=[
        DataRequired(), Length(max=150)])
    ticket_table_number = IntegerField('Table number', validators=[
        DataRequired(), NumberRange(min=0, max=1337)])
