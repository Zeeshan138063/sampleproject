"""Shared tasks placed here (Async)"""
from __future__ import absolute_import, unicode_literals

from celery import shared_task  # type: ignore
from celery import task   # type: ignore
from django.conf import settings
from django.template.loader import get_template
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from api.users.models import EmailStatus


@shared_task(name="sum_of_two_numbers")
def add(x, y):
    """Example task"""

    print(f"{x} + { y}= ")
    return x + y


@task()
def send_email():
    """Sending Email using Sengrid Client After every 1 minute"""
    url = settings.SITE_URL
    pending_users = EmailStatus.objects.filter(email_status=EmailStatus.STATUS.pending)
    for p_user in pending_users:
        message = Mail(
            from_email=settings.EMAIL_SENDER,
            to_emails=p_user.user_email.email,
            subject='Activation Account',
            html_content=get_template(
                'email/confirmation.html'
            ).render(
                {'uid': urlsafe_base64_encode(
                    force_bytes(p_user.user_email.pk)).encode().decode(),
                 'token': p_user.user_email.verification_code,
                 'url': url
                 }
            ))
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        try:
            sg.send(message)
            update_status = EmailStatus.objects.get(
                user_email__email=p_user.user_email.email)
            update_status.email_status = EmailStatus.STATUS.success
            update_status.save()
        except Exception as e:
            print(e)
            update_status = EmailStatus.objects.get(
                user_email__email=p_user.user_email.email)
            update_status.email_status = EmailStatus.STATUS.fail
            update_status.save()
