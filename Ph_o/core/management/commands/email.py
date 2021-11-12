from RunPhoto import settings
import os
from django.core.mail.message import EmailMultiAlternatives


def send_email(data):
    msg = EmailMultiAlternatives(data['subject'], data['text'], settings.EMAIL_HOST_USER,
                                 [data['email']])
    msg.attach_alternative(data['html'], "text/html")
    try:
        msg.attach_file(os.path.abspath(data['attach_file']))
    except:
        pass
    msg.send()
