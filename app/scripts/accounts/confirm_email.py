from sendgrid import Mail, SendGridAPIClient 
from config import config

def send_verification(to, subject, template):
    message = Mail(
        from_email = config.MAIL_DEFAULT_SENDER,
        to_emails = to,
        subject = subject,
        html_content = template
    )
    try:
        sendgrid_client = SendGridAPIClient(api_key = config.MAIL_PASSWORD)
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
        return None
    except Exception as e:
        print(e)
        return None
