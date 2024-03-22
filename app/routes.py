from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user, logout_user, current_user
from scripts.accounts import users, tokenizer, confirm_email
from scripts.experiments import experiments
from application import app

@app.route('/')
def index():
    '''Web application homepage.'''
    return render_template('index.html')


@app.route('/explore')
def explore():
    '''
    Page to explore and search for specific experiments.
    #TODO: 
        - Add logic to search the experiments database.
        - Functions to display list of experiments.
        - Page should have buttons to filter search results.
    '''
    return render_template('explore.html')


@app.route('/inactive')
@login_required
def inactive():
    '''Page to handle accounts that have not verified their emails.'''
    if current_user.isVerified is True:
        return redirect(url_for('index'))
    return render_template('accounts/inactive.html')


@app.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    '''
    Profile page.
    Users should be able to view their experiments, as well as upload and delete experiments.
    Additionally, should be able to alter/update user information should peers want to contact them.
    '''
    if current_user.isVerified is False:
        return redirect(url_for('inactive'))
    else:
        return render_template('accounts/profile.html', 
                               user_experiments = experiments.get_user_experiments(current_user.uuid))


@app.route('/confirm/<token>')
@login_required
def confirm(token):
    '''Page to handle account and email verification.'''
    try:
        email = tokenizer.confirm_token(token)
    except:
        flash('The confirmation link is invalid or expired.', 'danger')
    user = users.User.get_user(email)
    if user.isVerified is True:
        flash('This account has already been verified.')
        return redirect(url_for('profile'))
    else:
        user.isVerified = True
        users.User.verify(email)
        flash('Thank you for confirming your account! You should be redirected to your profile.')
        return redirect(url_for('profile'))


@app.route('/resend')
@login_required
def resend():
    '''Page to handle resending verification email.'''
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
    '''Publish page'''
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
