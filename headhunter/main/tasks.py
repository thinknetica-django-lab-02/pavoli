from datetime import datetime, timedelta
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.mail import EmailMultiAlternatives

from .models import Vacancy, Subscriber


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


def start():
    scheduler = BackgroundScheduler()
    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    scheduler.add_job(get_new_vacancy, 'cron', day_of_week='mon',
                      hour=5, minute=30, end_date='2021-05-30')
    scheduler.start()
