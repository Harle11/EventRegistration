import os
from flask import Flask
from flask_fontawesome import FontAwesome
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
fa=FontAwesome(app)

app.config['SECRET_KEY'] = 'ea75ae94f8a77cfdcaa52327cc384414'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///PhaseShift.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in first.'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('PS_MAIL_ID')
app.config['MAIL_PASSWORD'] = os.environ.get('PS_MAIL_PASS')
mail = Mail(app)

from phaseshift import routes