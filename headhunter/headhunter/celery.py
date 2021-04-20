import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'headhunter.settings')

app = Celery('headhunter')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send_new_vacancy": {
        "task": "main.tasks.get_new_vacancy_task",
        "schedule": crontab(hour=9, minute=0, day_of_week="sunday"),
    },
}
