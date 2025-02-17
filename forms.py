from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, ReadOnly, Disabled



class UserForm(FlaskForm):
    # id = IntegerField('Id', validators=[DataRequired()])
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    birth_year = IntegerField('Birth Year', validators=[DataRequired()])
    submit = SubmitField('Submit')

class JobForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    description = StringField('Description', validators=[DataRequired(), Length(min=2, max=200)])
    user_id = IntegerField('User Id', validators=[ReadOnly()])
    submit = SubmitField('Submit')

class CourseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    description = StringField('Description', validators=[DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Submit')

class EnrollForm(FlaskForm):
    course_id = IntegerField('Course Id', validators=[ReadOnly()])
    user_id = SelectMultipleField('Users Id', choices=[], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')