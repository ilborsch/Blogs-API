import smtplib
from email.message import EmailMessage
from app.config import SMTP_PASSWORD, SMTP_USER


SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


def validate_email(email: str):
    if not email:
        return False
    from re import search
    regex = r'^[a-z0-9]+[\._]?[ a-z0-9]+[@]\w+[. ]\w{2,3}$'
    return search(regex, email) is not None


def get_valid_email(email: str):
    return SMTP_USER if not validate_email(email) else email


def get_email_template_dashboard(username: str, user_email: str):
    print(username, user_email)
    email = EmailMessage()
    email['Subject'] = 'Blogs UA'
    email['From'] = SMTP_USER
    email['To'] = user_email

    email.set_content(
        '<div>'
        f'<h1 style="color: cyan;">Hello, {username}, nice to meet you! 😊</h1>'
        '<img src="https://i.pinimg.com/originals/cf/57/f3/cf57f39c151aa04dd525ec89713290e9.jpg" width="600">'
        '</div>',
        subtype='html'
    )
    return email


def send_greeting_email_task(username, user_email):
    email = get_email_template_dashboard(username, user_email)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)

