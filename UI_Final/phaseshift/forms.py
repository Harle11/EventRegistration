from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField, IntegerField
from wtforms.fields.html5 import TelField
from wtforms.validators import DataRequired, Email, ValidationError, Length
from phaseshift.models import *

class EventRegistrationForm(FlaskForm):
    eventName = StringField('Event Name', validators=[DataRequired()])
    fullname = TextAreaField('Full Name', validators=[DataRequired(), Length(min=3, message='Enter your full name with initials')])
    usn = TextAreaField('USN', validators=[DataRequired(), Length(min=5, message='Enter a valid USN or Student Registration Number')])
    college = StringField('College Name', validators=[DataRequired(), Length(min=2, message='Enter your college name or college initials')])
    email = StringField('Email ID', validators=[DataRequired(), Email()])
    phno = TelField('Phone No.', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_phno(form, phno):
        if len(phno.data) != 10:
            raise ValidationError('Enter a 10 digit phone number')
        elif int(phno.data[:1]) < 6:
            raise ValidationError('Enter a valid phone number')


class eventFilter(FlaskForm):
    all_events = Events.query.all()
    category = []
    for event in all_events:
        if event.etype not in category:
            category.append(event.etype)
    choices = [('All','All')]
    category.remove('Workshop')
    for i in range(len(category)):
        choices.append((category[i],category[i]))
    ch = SelectField('Event Type:', choices=choices)
    submit = SubmitField('Filter')

class LoginForm(FlaskForm):
    usn = StringField('USN', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    remember = BooleanField('Remeber Me')
    submit = SubmitField('Login')

class NewUser(FlaskForm):
    usn = StringField('USN', validators=[DataRequired(), Length(min=10, max=12, message='Enter a valid USN')])
    password = StringField('Password', validators=[DataRequired(), Length(min=6, message='Password needs to be at least 6 characters')])
    utype = SelectField('User Type', choices=[('Event Organizer','Event Organizer'),('Department Coordinator','Department Coordinator')])
    resp = StringField('Responsibility', validators=[DataRequired()])
    submit = SubmitField('Update User List')

class eventListFilter(FlaskForm):
    regs = EventRegistration.query.all()
    event_names = []
    for reg in regs:
        if reg.event_name not in event_names:
            event_names.append(reg.event_name)
    choices = [('None','None'), ('All','All')]
    for i in range(len(event_names)):
        choices.append((event_names[i],event_names[i]))
    ch = SelectField('Event Type:', choices=choices)
    submit = SubmitField('Filter')

class eventListFilterDC(FlaskForm):
    choices = [('None','None'), ('All','All')]
    ch = SelectField('Event Type:', choices=choices)
    submit = SubmitField('Filter')

class AddEventForm(FlaskForm):
    name = StringField('Name')
    evalue = StringField('EValue')
    etype = StringField('Type')
    dept = StringField('Department')
    desc = StringField('Description')
    rules = TextAreaField('Rules')
    fee = IntegerField('Fee')
    team_size = IntegerField('Team Size')
    date = StringField('Date')
    time = StringField('Time')
    venue = StringField('Venue')
    coordinators = StringField('Coordinators')
    prize = StringField('Prize')
    flagship = BooleanField('Flagship')
    submit = SubmitField('Submit')