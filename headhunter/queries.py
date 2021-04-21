import os
from datetime import datetime, timedelta

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'headhunter.settings')
django.setup()


def create_applicant():
    a = Applicant(first_name='John', last_name='Doe',
                  birth_date='1984-02-19', gender='m').save()
    b = Applicant(first_name='Elizabeth', last_name='Herley',
                  birth_date='1944-01-19', gender='f').save()
    c = Applicant(first_name='Elza', last_name='Bretanny',
                  birth_date='1974-11-25', gender='f').save()

    print('Applicant created')


def get_applicant_all():
    all_applicant = Applicant.objects.all()

    for i in all_applicant:
        print(f'Applicant: {i}')


def get_applicant(id):
    a = Applicant.objects.get(pk=id)
    print(a)

    return a


def get_applicant_by_filter(filter_name):
    a = Applicant.objects.filter(skill=filter_name)
    print(a)

    return a


def create_summary_main():
    a = get_applicant(1)

    SummaryMain.objects.bulk_create([
        SummaryMain(applicant=a,
                    title='Python Developer', salary=100000),
        SummaryMain(applicant=a,
                    title='Oracle Developer', salary=200000),
    ]
    )

    print(f'Summary created for user: {a}')


def get_summary_main_all():
    all_summary = SummaryMain.objects.all()

    for i in all_summary:
        print(f'Summary(head): {i}')


def create_skills():
    Technology.objects.bulk_create([
        Technology(name='Python'),
        Technology(name='Django Framework'),
        Technology(name='Django Rest Framework'),
        Technology(name='Docker'),
        Technology(name='MongoDB'),
        Technology(name='Redis'),
        Technology(name='Oracle'),
        Technology(name='Celery'),
        Technology(name='Go'),
    ])

    print('Skills created.')


def get_skill_fliter():
    for i in Technology.objects.filter(name__icontains='go'):
        print(i, end=', ')


def get_skills_all():
    for i in Technology.objects.all():
        print(i, end=', ')


def get_model_fields_name(model_name):
    print([f.name for f in model_name._meta.get_fields()])


def get_profile_table():
    profile = Profile.objects.all()
    for p in profile:
        print(f'profile={p}')


def fresh_vacancy():
    d = datetime.now()
    return [v.vacancy_name for v in Vacancy.objects.filter(publish_date__gte=d.date() - timedelta(days=7))]


def get_smslog():
    for s in SMSLog.objects.all():
        print(f'sms={s.code}, phone={s.phone_number}')


def create_smscode():
    import random
    sms_code = random.sample([str(x) for x in range(10)], 4)
    sms_code = ''.join(sms_code)

    print(f'sms_code={sms_code}')


def create_sms_task():
    from celery.utils.log import get_task_logger
    logger = get_task_logger(__name__)
    logger.info('Sending sms')
    import random
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
        print("Message sent successfully.")
    else:
        print(
            f"Message failed with error: {responseData['messages'][0]['error-text']}")


if __name__ == '__main__':
    from main.models import *

    # create_applicant()
    # get_applicant_all()
    # create_summary_main()
    # get_summary_main_all()
    # create_skills()
    # get_skill_fliter()
    # get_skills_all()
    # get_applicant_by_filter(filter_name=7)
    # get_model_fields_name(model_name=User)
    # get_profile_table()
    # print(fresh_vacancy())
    # get_smslog()
    # create_smscode()
    # create_sms_task()
    pass
