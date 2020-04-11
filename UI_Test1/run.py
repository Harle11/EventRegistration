from flask import Flask, render_template, url_for, flash, redirect
from flask_fontawesome import FontAwesome
from forms import *

app = Flask(__name__)
fa=FontAwesome(app)
app.config['SECRET_KEY'] = 'ea75ae94f8a77cfdcaa52327cc384414'

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

if __name__ == '__main__':
    app.run()