from flask import Flask
from flask_fontawesome import FontAwesome
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
fa=FontAwesome(app)

app.config['SECRET_KEY'] = 'ea75ae94f8a77cfdcaa52327cc384414'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PhaseShift.db'
db = SQLAlchemy(app)

from phaseshift import routes