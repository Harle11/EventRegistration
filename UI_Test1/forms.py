from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email, ValidationError, Length

class EventRegistrationForm(FlaskForm):
    eventName = StringField('Event Name', validators=[DataRequired()])
    fullname = TextAreaField('Full Name', validators=[DataRequired()])
    usn = TextAreaField('USN', validators=[DataRequired()])
    college = StringField('College Name', validators=[DataRequired()])
    email = StringField('Email ID', validators=[DataRequired(), Email()])
    phno = StringField('Phone No.', validators=[DataRequired(), Length(min=10, max=10, message='Enter a 10 digit phone number')])
    submit = SubmitField('Register')

class eventFilter(FlaskForm):
    ch = SelectField('Event Type:', choices=[('All','All'),('Coding','Coding'),('Treasure Hunt','Treasure Hunt'),('Presentation','Presentation')])
    submit = SubmitField('Filter')