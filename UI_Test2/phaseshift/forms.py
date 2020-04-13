from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError, Length
from phaseshift.models import Events, EventRegistration

class EventRegistrationForm(FlaskForm):
    eventName = StringField('Event Name', validators=[DataRequired()])
    fullname = TextAreaField('Full Name', validators=[DataRequired()])
    usn = TextAreaField('USN', validators=[DataRequired()])
    college = StringField('College Name', validators=[DataRequired()])
    email = StringField('Email ID', validators=[DataRequired(), Email()])
    phno = StringField('Phone No.', validators=[DataRequired(), Length(min=10, max=10, message='Enter a 10 digit phone number')])
    submit = SubmitField('Register')

class eventFilter(FlaskForm):
    all_events = Events.query.all()
    category = []
    for event in all_events:
        if event.etype not in category:
            category.append(event.etype)
    choices = [('All','All')]
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