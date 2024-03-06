from flask import Flask
import bcrypt
import os
from sendgrid import Mail, SendGridAPIClient 
#from application import app, mail

#Main Configuration
SECRET_KEY = bcrypt.hashpw(os.urandom(256), salt = bcrypt.gensalt()).decode('utf8')
SECURITY_PASSWORD_SALT = bcrypt.gensalt().decode('utf8')

#Gmail Authentication
MAIL_PASSWORD = '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'
MAIL_DEFAULT_SENDER = 'admin@cellportal.com'

def send_verification(to, subject, template):
    message = Mail(
        from_email = MAIL_DEFAULT_SENDER,
        to_emails = to,
        subject = subject,
        html_content = template
    )
    try:
        sendgrid_client = SendGridAPIClient(api_key = MAIL_PASSWORD)
        response = sendgrid_client.send(message)
        
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return None
    except Exception as e:
        print(e)
        return None

send_verification('wing_kin_chan@hotmail.com', 'Verify Test', 'This is a test')