# app.py
from flask import Flask, render_template, request, redirect
from scripts.db import users

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/publish', methods = ['GET', 'POST'])
def publish():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        response = users.new_user(email, password)
        if response == 'Email in use':
            return response
        else:
            return 'Check email to complete registration'
    return render_template('publish.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
