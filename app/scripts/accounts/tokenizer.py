'''
Token generation and email sending to provide account verification and prevent/deter
spam account generation.
'''

from itsdangerous import URLSafeTimedSerializer
from application import app

def generate_token(email: str):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt = app.config['SECURITY_PASSWORD_SALT'])

def confirm_token(token, expiration = 3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token, salt = app.config['SECURITY_PASSWORD_SALT'], max_age = expiration
        )
        return email
    except Exception:
        return False