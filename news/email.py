from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from django.template.loader import get_template

def send_welcome_email(name, reciever):
    # message subject and sender

    subject = 'Welcome to the Moringa Tribune Newsletter'
    sender = 'itsmisty41@gmail.com'

    # pass in the context variables

    text_content = render_to_string('all-news/email/newsemail.txt', {'name': name})
    html_content = render_to_string('all-news/email/newsemail.html', {'name': name})

    msg = EmailMultiAlternatives(subject,text_content, sender, [reciever])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()