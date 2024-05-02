import random
from .messaging_system import send_email
from django.template.loader import render_to_string

def generate_code():
    return random.randint(100000, 999999)

def email_verify(to, name, code):
    subject = f"Your verification code is {code}"
    context = {'code': code,}
    html_content = render_to_string('email_verify.html', context)
    send_email(to, name, subject, html_content)

def email_forgotten_password(to, name, code):
    subject = "CodeIA - Forgot your password?"
    link = "https://codeia-web.vercel.app/auth/password/reset/" + code
    context = {'link': link,}
    html_content = render_to_string('email_forgotten_password.html', context)
    send_email(to, name, subject, html_content)