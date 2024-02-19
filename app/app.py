# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from scripts.db import users
from config import config

login_manager = LoginManager()
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
login_manager.init_app(app)
login_manager.login_view = 'profile'

@login_manager.user_loader
def load_user(email):
    return users.get_user(email)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    return render_template('profile')

@app.route('/publish', methods = ['GET', 'POST'])
def publish():
    if request.method == 'POST':
        action = request.form.get('action')
        email = request.form.get('email')
        password = request.form.get('password')
        if action == 'login':
            if users.check_email_exists(email) == 0:
                return 'Email does not exist'
            credentials = users.get_hash(email)
            if users.hash_encode(password, credentials['salt'].__str__())[0] != credentials['password']:
                return 'Incorrect password'
            else:
                login_user(email)
                return redirect(url_for('profile'))
        elif action == 'register':
            return users.new_user(email, password)
    return render_template('publish.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
