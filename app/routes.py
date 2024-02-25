from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from scripts.accounts import users, token, email
from application import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile(user):
    if not user.isVerified:
        return redirect(url_for('inactive'))
    else:
        return render_template('profile')

@app.route('/confirm/<token>')
@login_required
def confirm(token_):
    try:
        email = token.confirm_token(token_)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = users.User.get_user(email)
    if user.isVerified:
        flash('Account has already been confirmed', 'success')
        return redirect(url_for('profile'))
    else:
        user.isVerified = True

@app.route('/publish', methods = ['GET', 'POST'])
def publish():
    if request.method == 'POST':
        action = request.form.get('action')
        email = request.form.get('email')
        password = request.form.get('password')
        if action == 'login':
            user = users.User.get_user(email)
            password_hash = users.hash_encode(password , user.salt.__str__())[0]
            if password_hash == user.password and user.isVerified:
                user.is_authenticated = True
                login_user(user)
                return redirect(url_for('profile'))
            elif password_hash == user.password:
                user.is_authenticated = True
                login_user(user)
                return redirect(url_for('inactive'))
            else:
                return 'Incorrect password.'
        elif action == 'register':
            users.User.create(email, password)
            new_token = token.generate_token(email)
            confirm_url = url_for('confirm', token_ = new_token, _external = True)
            html = render_template('activate.html', confirm_url = confirm_url)
            subject = 'cellPortal: Confirm Your Email'
            email.send_email(email, subject, html)
    return render_template('publish.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
