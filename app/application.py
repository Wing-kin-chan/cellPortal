from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from config import config
from scripts.accounts import users

app = Flask(__name__)
mail = Mail(app)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SECURITY_PASSWORD_SALT'] = config.SECURITY_PASSWORD_SALT
app.config['MAIL_DEFAULT_SENDER'] = config.MAIL_DEFAULT_SENDER

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'profile'

@login_manager.user_loader
def load_user(email):
    return users.User.get_user(email)