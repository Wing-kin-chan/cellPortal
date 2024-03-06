from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from config import config
from scripts.accounts import users

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SECURITY_PASSWORD_SALT'] = config.SECURITY_PASSWORD_SALT
app.config['MAIL_DEFAULT_SENDER'] = config.MAIL_DEFAULT_SENDER
app.config['MAIL_PORT'] = config.MAIL_PORT
app.config['MAIL_USE_TLS'] = config.MAIL_USE_TLS
app.config['MAIL_USE_SSL'] = config.MAIL_USE_SSL
app.config['MAIL_USERNAME'] = config.MAIL_USERNAME
app.config['MAIL_PASSWORD'] = config.MAIL_PASSWORD
mail = Mail(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'profile'

@login_manager.user_loader
def load_user(email):
    return users.User.get_user(email)