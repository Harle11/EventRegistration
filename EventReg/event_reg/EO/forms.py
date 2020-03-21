from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_login import current_user

class LoginForm(FlaskForm):
    usn = StringField('USN', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CreateUserForm(FlaskForm):
    usn = StringField('USN', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    #user_type = DropdownField('Registration','Event Head','Dept Head')
    submit = SubmitField('Create User')

    def validate_usn(self, usn):
        #user = db.users.find_one({'USN':form.usn.data},{'_id':0,'USN':1})
        if user:
            raise ValidationError('That student is already a user. Please enter a different usn.')

    #def validate_user_type(self, user_type):
        #user_level = db.users.find_one({'USN':user_usn},{'_id':0,'user_level':1})
        #if user_level <= user_type:
            #raise ValidationError('You cannot create users of greater or equal access. Choose a lower user type.')

class UpdateUserForm(FlaskForm):
    usn = StringField('USN', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    #user_type = DropdownField('Registration','Event Head','Dept Head')
    submit = SubmitField('Edit User Info')

    def validate_usn(self, usn):
        #user = db.users.find_one({'USN':form.usn.data},{'_id':0,'USN':1})
        if user:
            raise ValidationError('That student is already a user. Please enter a different usn.')

    #def validate_user_type(self, user_type):
        #user_level = db.users.find_one({'USN':user_usn},{'_id':0,'user_level':1})
        #if user_level <= user_type:
            #raise ValidationError('You cannot create users of greater or equal access. Choose a lower user type.')