from flask import Flask, render_template, url_for
from flask_fontawesome import FontAwesome

app = Flask(__name__)
fa=FontAwesome(app)

events = [
    {
        'name': 'Fishing Expedition',
        'evalue': 'fishing_expedition',
        'etype': 'Treasure Hunt',
        'team_size': '3'
    },
    {
        'name': 'Something Else',
        'evalue': 'something_else',
        'etype': 'Some Type',
        'team_size': '2'
    }
]

eflagship = [
    {
        'name': 'Flagship Event',
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
        'name': 'Workshop 1',
        'evalue': 'workshop_1',
        'dept': 'XYZ'
    },
    {
        'name': 'Some Flag Else',
        'evalue': 'something_else',
        'dept': 'ABC'
    }
]


@app.route("/")
def home():
    return render_template('home.html', events=events, eflagship=eflagship, eworkshops=eworkshops)


@app.route("/all-events")
def all_events():
    return render_template('general-events.html', events=events, title='All Events')

@app.route("/flagship")
def flagship():
    return render_template('flagship-events.html', eflagship=eflagship, title='Flagship Events')

@app.route("/workshops")
def workshops():
    return render_template('workshops.html', eworkshops=eworkshops, title='Workshops')

@app.route("/registration/<eventName>")
def registration(eventName):
    for event in events:
        if eventName == event['evalue']:
            return render_template('event-details.html', title='Event Details', event=event)
    return render_template('404.html', title='Page not found', message='No such event exists')

if __name__ == '__main__':
    app.run()