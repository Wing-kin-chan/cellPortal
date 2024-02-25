from flask_mail import Message
from application import app, mail

def send_email(to, subject, template):
    message = Message(
        subject,
        recipients = [to],
        html = template,
        sender = app.config.MAIL_DEFAULT_SENDER
    )
    mail.send(message)