from flask import render_template, url_for, flash, redirect, Blueprint
#from flask_login import login_user, current_user, logout_user, login_required
#from event_reg import bcrypt
from event_reg.EO.forms import (LoginForm, CreateUserForm, UpdateUserForm)

EO = Blueprint('EO',__name__)

@EO.route("/EO")
@EO.route('/EO/login', methods=['GET','POST'])
def login():
    #if current_user.is_authenticated:
        #return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        #user = db.users.find_one({'USN':form.usn.data},{'_id':0,'USN':1})
        #pass = db.users.find_one({'USN':form.usn.data},{'_id':0,'pass':1})
        #if user and bcrypt.check_password_hash(pass, form.password.data):
            #login_user(user, remember=form.remember.data)
            return redirect(url_for('EO.home'))
        else:
            flash('Login Unsuccessful. Please check USN and password', 'danger')
    return render_template('EO/login.html', title='Login', form=form)


@EO.route("/EO/home")
#@login_required
def home():
    return render_template('EO/home.html')

@EO.route("/EO/NewUser",  methods=['GET','POST'])
#@login_required
def newUser():
    form = CreateUserForm()
    if form.validate_on_submit():
        flash('User created successfully!','success')
    return render_template('EO/newUser.html', title='New User', form=form)

@EO.route("/EO/EditUser",  methods=['GET','POST'])
#@login_required
def editUser():
    form - UpdateUserForm()
    if form.validate_on_submit():
        flash('User info edited successfully!','success')
    return render_template('EO/editUser.html', title='Edit User', form=form)

@EO.route("/EO/registrations")
#@login_required
def registrations():
    return render_template('EO/viewRegistrations.html')

@EO.route("/EO/logout")
def logout():
    #logout_user()
    return redirect(url_for('EO.login'))

