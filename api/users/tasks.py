"""Shared tasks placed here (Async)"""
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.conf import settings
from django.template.loader import get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from api.users.models import User


@shared_task(name="sum_of_two_numbers")
def add(x, y):
    """Example task"""

    print(f"{x} + { y}= ")
    return x + y


@shared_task(name="email_sending")
def send_email(u_id):
    """Sending Email using Sengrid Client"""

    url = settings.SITE_URL
    user = User.objects.get(pk=u_id)
    message = Mail(
        from_email=settings.EMAIL_SENDER,
        to_emails=user.email,
        subject='Activation Account',
        html_content=get_template(
            'email/confirmation.html'
        ).render(
            {'uid': urlsafe_base64_encode(
                force_bytes(user.pk)).encode().decode(),
             'token': user.verification_code,
             'url': url
             }
        ))
    sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
    try:
        sg.send(message)
    except Exception as e:
        print(e)
