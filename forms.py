from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class UserForm(FlaskForm):
    id = IntegerField('Id', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    birth_year = IntegerField('Birth Year', validators=[DataRequired()])
    submit = SubmitField('Submit')