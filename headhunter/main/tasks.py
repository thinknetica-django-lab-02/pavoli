from datetime import datetime, timedelta
import logging

from django.core.mail import EmailMultiAlternatives
from celery.utils.log import get_task_logger
from celery import shared_task

from .models import Vacancy, Subscriber
from headhunter.celery import app


logger = get_task_logger(__name__)


def get_new_vacancy():
    d = datetime.now()

    email_list = [s.user.email for s in Subscriber.objects.all()]
    fresh_vacancy = [v.vacancy_name for v in Vacancy.objects.filter(
        publish_date__gte=d.date() - timedelta(days=7))]
    subject = 'Fresh Vacancies'
    from_email = 'admin@mysite'
    text_content = 'Vacancy List'
    html_content = f'''
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
  </head>
  <body>
    <p>Vacancy List:</p>
    {fresh_vacancy}
  </body>
</html>
    '''
    msg = EmailMultiAlternatives(
        subject, text_content, from_email, email_list)
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@shared_task
def get_new_vacancy_task():
    logger.info('Sent new vacancy lists.')
    return get_new_vacancy
