import smtplib
from email.message import EmailMessage
from celery import Celery
from app.config import SMTP_PASSWORD, SMTP_USER
from app.config import REDIS_HOST, REDIS_PORT

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery_app = Celery('tasks', broker=f"{REDIS_HOST}:{REDIS_PORT}")


def validate_email(email: str):
    if not email:
        return False
    from re import search
    regex = r'^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$'
    return search(regex, email) is not None


def get_valid_email(email: str):
    return SMTP_USER if not validate_email(email) else email


def get_email_template_dashboard(username: str, user_email: str):
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


@celery_app.task
def send_greeting_email_task(username, user_email):
    email = get_email_template_dashboard(username, user_email)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)

