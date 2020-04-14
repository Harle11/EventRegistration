from flask import render_template, url_for, flash, redirect
from phaseshift import app, db
from phaseshift.models import Users, Events, EventRegistration
from phaseshift.forms import *

events = [
    {
        'name': 'Fishing Expedition',
        'evalue': 'fishing_expedition',
        'etype': 'Treasure Hunt',
        'dept': 'MCA',
        'desc': 'Participants are requested to be aware of ASCII values. Round1: Reframing the code using the ASCII values. Round2: Debugging the html code and finding clues for the successive HTML files and finally reach the destination file.',
        'fee': 200,
        'team_size': 3,
        'date': '15/09/2019',
        'time': '1pm - 5pm',
        'venue': 'MCA Lab, PG Block',
        'coordinators': 'Anitha B#9741175438#Prajwal M P#9900806532',
        'prize': 'Rs.4000 for winners & Rs.2000 for runner-up',
        'workshop': False
    },
    {
        'name': 'Dazzle Coding',
        'evalue': 'dazzle_coding',
        'etype': 'Coding',
        'dept': 'MCA',
        'desc': 'The participants will have to solve the problem with the monitor switched off.',
        'fee': 100,
        'team_size': 1,
        'date': '15/09/2019',
        'time': '9am - 12pm',
        'venue': 'MCA Lab, PG Block',
        'coordinators': 'Anamika Tripati#7039812192#Manasa M N#9731803047',
        'prize': 'Rs.3000 for winners & Rs.1500 for runner-up',
        'workshop': False
    },
    {
        'name': 'Sliders',
        'evalue': 'sliders',
        'etype': 'Presentation',
        'dept': 'MCA',
        'desc': 'Every team will be given a topic to present on. 5 slides max and 5 mins presentation time. Participants will be given 30 mins to prepare their slides.',
        'fee': 100,
        'team_size': 2,
        'date': '14/09/2019',
        'time': '11am - 2pm',
        'venue': 'MCA Lab, PG Block',
        'coordinators': 'Bharath P G#8050568616#Ranjitha S#7411840130',
        'prize': 'Rs.3000 for winners & Rs.1500 for runner-up',
        'workshop': False
    },
    {
        'name': 'Zeal',
        'evalue': 'zeal',
        'dept': 'MCA',
        'desc': 'Workshop on energy conservation using technology',
        'fee': 100,
        'date': '14/09/2019',
        'time': '1pm - 5pm',
        'venue': 'FDC Hall, PG Block',
        'coordinators': 'Kashish Singh#7406054057#Gowda Pooja Umesh#9448645828',
        'workshop': True
    },
    {
        'name': 'Some Flag Else',
        'evalue': 'something_flag_else',
        'dept': 'ABC',
        'workshop': True
    }
]

eflagship = [
    {
        'name': 'Fishing Expedition',
        'evalue': 'fishing_expedition',
        'etype': 'Treasure Hunt',
        'team_size': '3',
        'dept': 'XYZ'
    },
    {
        'name': 'Some Flag Else',
        'evalue': 'something_else',
        'etype': 'Some Type',
        'team_size': '2',
        'dept': 'ABC'
    }
]

eworkshops = [
    {
        'name': 'Zeal',
        'evalue': 'zeal',
        'dept': 'MCA'
    },
    {
        'name': 'Some Flag Else',
        'evalue': 'something_flag_else',
        'dept': 'ABC'
    }
]


@app.route("/")
def home():
    return render_template('home.html', events=events, eflagship=eflagship, eworkshops=eworkshops)

@app.route("/organizer/login", methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(usn=form.usn.data).first()
        if user and user.password == form.password.data:
            if user.utype == 'admin':
                flash('Welcome Admin', 'success')
                return redirect(url_for('admin_home', filters='None'))
            else:
                flash('Welcome {}-{}'.format(user.utype,user.usn),'success')
                return redirect(url_for('org_home', filters='None', user=user.id))
        flash('Incorrect USN or Password','danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/organizer/logout")
def logout():
    flash('Succesfully logged out', 'success')
    return redirect(url_for('login'))

@app.route("/organizer/admin/userlist/<usnx>", methods=['GET','POST'])
def admin_add_user(usnx):
    user = Users.query.filter_by(usn=usnx).first()
    form = NewUser()
    usn1 = uresp = ""
    if form.validate_on_submit():
        if user:
            user.password = form.password.data
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
            u1 = Users(usn=form.usn.data, password=form.password.data, utype=form.utype.data, responsibility=form.resp.data)
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
def admin_delete_user(usnx):
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
def admin_home(filters):
    form = eventListFilter(ch=filters)
    if form.validate_on_submit():
        return redirect(url_for('admin_home', filters=form.ch.data))
    all_users=Users.query.order_by(Users.usn).all()
    all_users=all_users[:-1]
    regs = ''
    if filters != 'None' and filters != 'All':
        regs = EventRegistration.query.filter_by(event_name=filters).order_by(EventRegistration.stud_name).all()
        if regs:
            return render_template('admin_home.html', title='Admin Home', all_users=all_users, filters=filters, regs=regs, form=form)
        else:
            return render_template('404.html', title='Error 404', message='Unknown event name')
    elif filters == 'All':
        regs = EventRegistration.query.order_by(EventRegistration.event_name,EventRegistration.stud_name).all()
    return render_template('admin_home.html', title='Admin Home', all_users=all_users, filters=filters, regs=regs, form=form)

@app.route("/organizer/<user>/<filters>", methods=['GET','POST'])
def org_home(user, filters):
    user=Users.query.filter_by(id=user).first()
    eventnames = []
    form = eventListFilterDC(ch=filters)
    if user:
        if user.utype == 'Department Coordinator':
            choices = form.ch.choices
            all_events = Events.query.filter_by(dept=user.responsibility)
            for event in all_events:
                if event.name not in eventnames:
                    eventnames.append(event.name)
            for i in range(len(eventnames)):
                choices.append((eventnames[i],eventnames[i]))
            form.ch.choices = choices
        else:
            choices = form.ch.choices
            choices = choices[:-1]
            choices.append((user.responsibility,user.responsibility))
    else:
        form = eventListFilter(ch=filters)
    if form.validate_on_submit():
        return redirect(url_for('org_home', user=user.id, filters=form.ch.data))
    regs = []
    if filters != 'None' and filters != 'All':
        regs = EventRegistration.query.filter_by(event_name=filters).order_by(EventRegistration.stud_name).all()
        if regs:
            return render_template('org_home.html', title='Organizer Home', regs=regs, user=user, filters=filters, form=form)
        else:
            return render_template('404.html', title='Error 404', message='Unknown event name. Contact Admin.')
    '''elif filters == 'All':
        for event in eventnames:
            regs.append(EventRegistration.query.filter_by(event_name=event).order_by(EventRegistration.event_name,EventRegistration.stud_name).all())'''
    return render_template('org_home.html', title='Organizer Home', filters=filters, user=user, regs=regs, form=form)

@app.route("/all-events/<choice>", methods=['GET','POST'])
def all_events(choice):
    form = eventFilter(ch=choice)
    if form.validate_on_submit():
        return redirect(url_for('all_events', choice=form.ch.data))
    for event in events:
        if choice == event['etype'] or choice == 'All':
            return render_template('general-events.html', events=events, title='All Events', choice=choice, form=form)
    return render_template('404.html', title='Page not found', message='No such event type exists')

@app.route("/flagship")
def flagship():
    return render_template('flagship-events.html', eflagship=eflagship, title='Flagship Events')

@app.route("/workshops")
def workshops():
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
        flash('You have successfully registered for {}. Register for more events below!'.format(form.eventName.data), 'success')
        return redirect(url_for('all_events', choice='All'))
    for event in events:
        if eventName == event['name']:
            isworkshop = False
            cords = []
            teamSize = '1'
            if event['workshop']:
                isworkshop = True
            else:
                teamSize = str(event['team_size'])
            for x in event['coordinators'].split('#'):
                    cords.append(x)
            return render_template('event-details.html', title='Event Details', event=event, isworkshop=isworkshop, cords=cords, len=len(cords), form=form, teamSize=teamSize)
    return render_template('404.html', title='Page not found', message='No such event exists')
