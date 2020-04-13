from phaseshift import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usn = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    utype = db.Column(db.String(20), nullable=False)
    responsibility = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "User({}, {}, {})".format(self.usn, self.utype, self.responsibility)

class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    etype = db.Column(db.String(50), nullable=False)
    dept = db.Column(db.String(30), nullable=False)
    desc = db.Column(db.String(200), nullable=False)
    fee = db.Column(db.String(5), nullable=False)
    team_size = db.Column(db.Integer, nullable=False, default=1)
    date = db.Column(db.String(15), nullable=False)
    time = db.Column(db.String(15), nullable=False)
    venue = db.Column(db.String(50), nullable=False)
    coordinators = db.Column(db.String(100), nullable=False)
    prize = db.Column(db.String(50), nullable=False)
    workshop = db.Column(db.Boolean, nullable=False, default=False)
    flagship = db.Column(db.Boolean, nullable=False, default=False)
    registered = db.relationship('EventRegistration', backref='regEvent', lazy=True)

    def __repr__(self):
        return "Event details({}, {}, {})".format(self.name, self.etype, self.dept)
    
class EventRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    event_name = db.Column(db.String(100), nullable=False)
    stud_name = db.Column(db.Text, nullable=False)
    stud_usn = db.Column(db.Text, nullable=False)
    stud_college = db.Column(db.String(100), nullable=False)
    stud_email = db.Column(db.String(100), nullable=False)
    stud_phno = db.Column(db.String(15), nullable=False)
    paid = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return "Registration({}, {}, {})".format(self.event_name, self.stud_name, self.stud_usn)