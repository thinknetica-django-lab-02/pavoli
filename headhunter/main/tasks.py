from datetime import datetime, timedelta
import logging
import random

from django.core.mail import EmailMultiAlternatives
from celery.utils.log import get_task_logger
from celery import shared_task

from .models import Vacancy, Subscriber, SMSLog
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


@shared_task
def create_sms_task():
    logger.info('Sending sms')
    sms_code = random.sample([str(x) for x in range(10)], 4)
    sms_code = ''.join(sms_code)
    cell_phone = '79219935443'

    import vonage

    client = vonage.Client(key="999f0f38", secret="yd8FzNA1zaqOY2bj")
    sms = vonage.Sms(client)

    responseData = sms.send_message(
        {
            "from": "Vonage APIs",
            "to": cell_phone,
            "text": sms_code,
        }
    )

    server_responde = responseData["messages"][0]["status"]

    a = SMSLog(phone_number=cell_phone, code=sms_code,
               server_response=server_responde).save()

    if server_responde == "0":
        logger.info('Message sent successfully.')
    else:
        error_msg = responseData['messages'][0]['error-text']
        logger.info(f"Message failed with error: {error_msg}")
