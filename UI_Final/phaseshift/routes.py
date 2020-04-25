from flask import render_template, url_for, flash, redirect
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from sqlalchemy.sql import func
from phaseshift import app, db, bcrypt, mail
from phaseshift.models import *
from phaseshift.forms import *

@app.route("/")
def home():
    events = Events.query.filter(Events.etype!='Workshop', Events.flagship==False).order_by(func.random()).limit(8).all()
    eflagship = Events.query.filter_by(flagship=True).order_by(func.random()).limit(6).all()
    eworkshops = Events.query.filter_by(etype='Workshop').order_by(func.random()).limit(6).all()
    return render_template('home.html', events=events, eflagship=eflagship, eworkshops=eworkshops)

@app.route("/organizer/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        if current_user.utype == 'admin':
            return redirect(url_for('admin_home', filters='None'))
        else:
            return redirect(url_for('org_home', filters='None', user=current_user.id))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(usn=form.usn.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.utype == 'admin':
                login_user(user, remember=form.remember.data)
                flash('Welcome Admin', 'success')
                return redirect(url_for('admin_home', filters='None'))
            else:
                login_user(user, remember=form.remember.data)
                flash('Welcome {}-{}'.format(user.utype,user.usn),'success')
                return redirect(url_for('org_home', filters='None', user=user.id))
        flash('Incorrect USN or Password','danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/organizer/logout")
@login_required
def logout():
    logout_user()
    flash('Succesfully logged out', 'success')
    return redirect(url_for('login'))

@app.route("/organizer/admin/userlist/<usnx>", methods=['GET','POST'])
@login_required
def admin_add_user(usnx):
    if current_user.is_authenticated:
        if current_user.utype != 'admin':
            flash('You do not have access to that page', 'danger')
            return redirect(url_for('login'))
    user = Users.query.filter_by(usn=usnx).first()
    form = NewUser()
    usn1 = uresp = ""
    if form.validate_on_submit():
        if user:
            user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.utype = form.utype.data
            user.responsibility = form.resp.data
            db.session.commit()
            flash('User {} successfully updated'.format(form.usn.data), 'success')
            return redirect(url_for('admin_home', filters='None'))
        else:
            exists = Users.query.filter_by(usn=form.usn.data).first()
            if exists:
                flash('User {} already has a responsibility({}). Give a different user\'s USN'.format(form.usn.data, exists.responsibility), 'danger')
                return redirect(url_for('admin_add_user', usnx='Add-User'))
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            u1 = Users(usn=form.usn.data, password=hashed_password, utype=form.utype.data, responsibility=form.resp.data)
            db.session.add(u1)
            db.session.commit()
            flash('User {} having responsibility \'{}\' successfully added'.format(form.usn.data,form.resp.data), 'success')
            return redirect(url_for('admin_home', filters='None'))
    else:
        if user:
            password = form.password.data
            if password and len(password) < 6:
                flash('Password too short, unable to update.', 'danger')
                return redirect(url_for('admin_add_user', usnx=user.usn))
    if user:
        form = NewUser(utype=user.utype)
        usn1 = user.usn
        uresp = user.responsibility
    return render_template('admin_user.html', title='Add User', form=form, usn1=usn1, uresp=uresp)

@app.route("/organizer/admin/delete/<usnx>", methods=['GET'])
@login_required
def admin_delete_user(usnx):
    if current_user.is_authenticated:
        if current_user.utype != 'admin':
            flash('You do not have access to that page', 'danger')
            return redirect(url_for('login'))
    user = Users.query.filter_by(usn=usnx).first()
    if user:
        usn = user.usn
        uid = Users.query.get_or_404(user.id)
        db.session.delete(uid)
        db.session.commit()
        flash('User {} successfully deleted'.format(usn), 'success')
        return redirect(url_for('admin_home', filters='None'))
    else:
        flash('Something went wrong try again', 'danger')
        return redirect(url_for('admin_home', filters='None'))

@app.route("/organizer/admin/<filters>", methods=['GET','POST'])
@login_required
def admin_home(filters):
    if current_user.is_authenticated:
        if current_user.utype != 'admin':
            flash('You do not have access to that page', 'danger')
            return redirect(url_for('login'))
    form = eventListFilter(ch=filters)
    if form.validate_on_submit():
        return redirect(url_for('admin_home', filters=form.ch.data))
    all_users=Users.query.order_by(Users.usn).all()
    user_list=[]
    for u in all_users:
        if u.utype != 'admin':
            user_list.append(u)
    regs = ''
    if filters != 'None' and filters != 'All':
        regs = EventRegistration.query.filter_by(event_name=filters).order_by(EventRegistration.stud_name).all()
        if regs:
            return render_template('admin_home.html', title='Admin Home', all_users=user_list, filters=filters, regs=regs, form=form)
        else:
            return render_template('404.html', title='Error 404', message='Unknown event name')
    elif filters == 'All':
        regs = EventRegistration.query.order_by(EventRegistration.event_name,EventRegistration.stud_name).all()
    return render_template('admin_home.html', title='Admin Home', all_users=user_list, filters=filters, regs=regs, form=form)

@app.route("/organizer/<user>/<filters>", methods=['GET','POST'])
@login_required
def org_home(user, filters):
    if current_user.is_authenticated:
        if str(current_user.id) != str(user):
            flash('You don\'t have access to that page', 'danger')
            return redirect(url_for('login'))
    eventnames = []
    form = eventListFilterDC(ch=filters)
    if current_user.utype == 'Department Coordinator':
        choices = form.ch.choices
        all_events = Events.query.filter_by(dept=current_user.responsibility)
        for event in all_events:
            if event.evalue not in eventnames:
                eventnames.append(event.evalue)
        for i in range(len(eventnames)):
            choices.append((eventnames[i],eventnames[i]))
        form.ch.choices = choices
    else:
        choices = form.ch.choices
        choices = choices[:-1]
        resp = current_user.responsibility
        choices.append((resp,resp))
        form.ch.choices = choices
    if form.validate_on_submit():
        return redirect(url_for('org_home', user=current_user.id, filters=form.ch.data))
    regs = []
    if filters != 'None' and filters != 'All':
        regs = EventRegistration.query.filter(EventRegistration.regEvent.has(evalue=filters)).order_by(EventRegistration.stud_name).all()
        if regs:
            return render_template('org_home.html', title='Organizer Home', regs=regs, user=current_user.id, filters=filters, form=form)
        else:
            event = Events.query.filter_by(evalue=filters).first()
            if event:
                return render_template('org_home.html', title='Organizer Home', regs=regs, user=current_user.id, filters=filters, form=form)
            else:
                return render_template('404.html', title='Error 404', message='Unknown event name. Contact Admin.'), 404
    elif filters == 'All':
        regs = EventRegistration.query.filter(EventRegistration.regEvent.has(dept=current_user.responsibility)).order_by(EventRegistration.event_name,EventRegistration.stud_name).all()
    return render_template('org_home.html', title='Organizer Home', filters=filters, user=user, regs=regs, form=form)

@app.route("/all-events/<choice>", methods=['GET','POST'])
def all_events(choice):
    form = eventFilter(ch=choice)
    if form.validate_on_submit():
        return redirect(url_for('all_events', choice=form.ch.data))
    events = Events.query.filter(Events.etype!='Workshop').order_by(Events.name).all()
    for event in events:
        if choice == event.etype or choice == 'All':
            return render_template('general-events.html', events=events, title='All Events', choice=choice, form=form)
    return render_template('404.html', title='Page not found', message='No such event type exists')

@app.route("/flagship")
def flagship():
    eflagship = Events.query.filter_by(flagship=True).order_by(Events.name).all()
    return render_template('flagship-events.html', eflagship=eflagship, title='Flagship Events')

@app.route("/workshops")
def workshops():
    eworkshops = Events.query.filter_by(etype='Workshop').order_by(Events.name).all()
    return render_template('workshops.html', eworkshops=eworkshops, title='Workshops')

@app.route("/registration/<eventName>", methods=['GET','POST'])
def registration(eventName):
    form = EventRegistrationForm()
    if form.validate_on_submit():
        reg_event = Events.query.filter_by(name=form.eventName.data).first()
        eventID = reg_event.id
        reg = EventRegistration(event_id=eventID,event_name=form.eventName.data,stud_name=form.fullname.data,stud_usn=form.usn.data,stud_college=form.college.data,stud_email=form.email.data,stud_phno=form.phno.data)
        db.session.add(reg)
        db.session.commit()
        send_registration_mail(reg)
        flash('You have successfully registered for {}. You should have received a mail confirming your registration.\nRegister for more events below!'.format(form.eventName.data), 'success')
        return redirect(url_for('all_events', choice='All'))
    events = Events.query.all()
    for event in events:
        if eventName == event.name:
            isworkshop = False
            cords = []
            teamSize = '1'
            if event.etype == 'Workshop':
                isworkshop = True
            else:
                teamSize = str(event.team_size)
            for x in event.coordinators.split('#'):
                    cords.append(x)
            return render_template('event-details.html', title='Event Details', event=event, isworkshop=isworkshop, cords=cords, len=len(cords), form=form, teamSize=teamSize)
    return render_template('404.html', title='Page not found', message='No such event exists')

def send_registration_mail(reg):
    msg = Message('PhaseShift Registration', sender='ps.registrations@yahoo.com', recipients=[reg.stud_email])
    names = reg.stud_name.split('\r\n')
    usns = reg.stud_usn.split('\r\n')
    allnames = names[0]
    allusns = usns[0]
    for i in range(1,len(names)):
        allnames = allnames + ', ' + names[i]
        allusns = allusns + ', ' + usns[i]
    msg.body = '''Hi {},

This is a message from BMSCE PhaseShift acknowledging your registration for the {} event.
Here are the details:
    Event Name: {}
    Student Name(s): {}
    Student USN(s): {}
    College: {}

Show this message at the venue to confirm your participation.
Have a great day and good luck in your event!

If you did not register for an event and received this mail, kindly ignore this mail.'''.format(allnames, reg.event_name, reg.event_name, allnames, allusns, reg.stud_college)
    mail.send(msg)

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html', title='404 Error'), 404

@app.errorhandler(403)
def error_403(error):
    return render_template('403.html', title='403 Error'), 403

@app.errorhandler(500)
def error_500(error):
    return render_template('500.html', title='Server Error'), 500

@app.route("/add-edit-events/<eventx>", methods=['GET','POST'])
@login_required
def add_edit_events(eventx):
    if current_user.is_authenticated:
        if current_user.utype != 'admin':
            flash('You do not have access to that page', 'danger')
            return redirect(url_for('login'))
    event = Events.query.filter_by(evalue=eventx).first()
    form = AddEventForm()
    if form.validate_on_submit():
        if event:
            event.name = form.name.data
            event.evalue = form.evalue.data
            event.etype = form.etype.data
            event.dept = form.dept.data
            event.desc = form.desc.data
            event.rules = form.rules.data
            event.fee = form.fee.data
            event.team_size = form.team_size.data
            event.date = form.date.data
            event.time = form.time.data
            event.venue = form.venue.data
            event.coordinators = form.coordinators.data
            event.prize = form.prize.data
            event.flagship = form.flagship.data
            db.session.commit()
            flash('{} successfully updated'.format(form.name.data), 'success')
            return redirect(url_for('myevents'))
        else:
            e1 = Events(name=form.name.data, evalue=form.evalue.data, etype=form.etype.data, dept=form.dept.data, desc=form.desc.data, rules=form.rules.data, fee=form.fee.data, team_size=form.team_size.data, date=form.date.data, time=form.time.data, venue=form.venue.data, coordinators=form.coordinators.data, prize=form.prize.data, flagship=form.flagship.data)
            db.session.add(e1)
            db.session.commit()
            flash('{} successfully added'.format(form.name.data), 'success')
            return redirect(url_for('myevents'))
    eve = None
    if event:
        eve = event
    return render_template('event_add.html', title='Update Event', eve=eve, form=form)

@app.route("/delete-event/<eventx>")
@login_required
def delete_event(eventx):
    if current_user.is_authenticated:
        if current_user.utype != 'admin':
            flash('You do not have access to that page', 'danger')
            return redirect(url_for('login'))
    event = Events.query.filter_by(name=eventx).first()
    if event:
        ename = event.name
        eid = Events.query.get_or_404(event.id)
        db.session.delete(eid)
        db.session.commit()
        flash('Event {} successfully deleted'.format(ename), 'success')
        return redirect(url_for('myevents'))
    else:
        flash('Something went wrong try again', 'danger')
        return redirect(url_for('myevents'))

@app.route("/myevents")
@login_required
def myevents():
    if current_user.is_authenticated:
        if current_user.utype != 'admin':
            flash('You do not have access to that page', 'danger')
            return redirect(url_for('login'))
    all_eves=Events.query.order_by(Events.name).all()
    return render_template('myevents.html', title='All events', all_eves=all_eves)
