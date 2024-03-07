from functools import wraps

from flask import flash, redirect, url_for
from flask_login import current_user

def check_user_verified(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        if current_user.isVerified is False:
            flash('Account not verified', 'warning')
            return redirect(url_for('inactive'))
        return function(*args, **kwargs)
    return decorated_function