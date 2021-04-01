import django
import os

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
    pass
