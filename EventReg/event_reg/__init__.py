from flask import Flask
#from flask_bcrypt import Bcrypt
#from flask_login import LoginManager
#from flask_mail import Mail
from event_reg.config import Config

#bcrypt = Bcrypt()
#login_manager = LoginManager()
#login_manager.login_view = 'EO.login'
#login_manager.login_message_category = 'info'
#mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    #bcrypt.init_app(app)
    #login_manager.init_app(app)
    #mail.init_app(app)

    from event_reg.EO.routes import EO
    from event_reg.RS.routes import RS
    from event_reg.errors.routes import errors
    app.register_blueprint(EO)
    app.register_blueprint(RS)
    app.register_blueprint(errors)

    return app