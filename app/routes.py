from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from scripts.accounts import users, tokenizer, confirm_email
from application import app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    if not current_user.isVerified:
        return redirect(url_for('inactive'))
    else:
        return render_template('accounts/profile')

@app.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.isVerified:
        flash('Account has already been confirmed', 'success')
        return redirect(url_for('profile'))
    user = users.User.get_user(current_user.email)
    email = tokenizer.confirm_token(token)
    if user.email == email:
        users.User.verify(user.email)
        flash('Email confirmed! You should be redirected to your profile.')
        return redirect(url_for('profile'))
    else:
        flash('The confirmation link is invalid or has expired.', 'danger')
        logout_user()
        return redirect(url_for('index'))


@app.route('/inactive')
@login_required
def inactive():
    if current_user.isVerified:
        return redirect(url_for('index'))
    return render_template('accounts/inactive.html')

@app.route('/resend')
@login_required
def resend():
    if current_user.isVerified:
        return redirect(url_for('index'))
    new_token = tokenizer.generate_token(current_user.email)
    confirm_url = url_for('confirm', token = new_token, _external = True)
    html = render_template('accounts/confirm.html', confirm_url = confirm_url)
    subject = 'cellPortal: Confirm Your Email'
    confirm_email.send_verification(current_user.email, subject, html)
    return redirect(url_for('inactive'))

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

            new_token = tokenizer.generate_token(email)
            confirm_url = url_for('confirm', token = new_token, _external = True)
            html = render_template('accounts/confirm.html', confirm_url = confirm_url)
            subject = 'cellPortal: Confirm Your Email'
            confirm_email.send_verification(email, subject, html)

            user = users.User.get_user(email)
            login_user(user)
            return redirect(url_for('inactive'))
    return render_template('publish.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
