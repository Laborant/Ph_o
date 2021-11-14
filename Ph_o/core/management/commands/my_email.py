from RunPhoto import settings
import os
from django.core.mail.message import EmailMultiAlternatives
from django.core.mail import send_mail


def send_email(data):
    try:
        msg = EmailMultiAlternatives(data['subject'], data['text'], settings.EMAIL_HOST_USER,
                                 [data['email']])
        try:
            msg.attach_alternative(data['html'], "text/html")
        except:
            pass
        try:
            msg.attach_file(os.path.abspath(data['attach_file']))
        except:
            pass
        msg.send()
    except:
        send_mail(
            data['subject'],
            data['text'],
            settings.EMAIL_HOST_USER,
            [data['email']],
            fail_silently=False,
        )



