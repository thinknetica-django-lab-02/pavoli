from allauth.account.signals import user_signed_up

from django.contrib.auth.models import Group, User
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpRequest, HttpResponse
from django.urls import reverse

from sorl.thumbnail import ImageField


# Create your models here.
CURRENCY_CHOICE = (
    ('r', 'RUB'),
    ('e', 'EUR'),
    ('u', 'USD'),
)


class Technology(models.Model):

    name = models.CharField(
        max_length=100, help_text='Enter a technology name')

    def __str__(self) -> HttpResponse:
        return '{0}(id={1})'.format(self.name, self.id)


class Applicant(models.Model):
    """Model for Candidates whose can have 1 or more Summary.
    """

    GENDER_CHOICE = (
        ('m', 'male'),
        ('f', 'female'),
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, blank=True)
    skill = models.ManyToManyField(
        Technology, help_text="Select a skill for Candidate")
    image = ImageField(upload_to='images', blank=True, null=True)

    def get_absolute_url(self) -> HttpResponse:
        return reverse('applicant-detail', args=[str(self.id)])

    def __str__(self) -> str:
        """Print class in human-readeable format.
        You can add/remove class-fields.

        :return: str
        :rtype: str
        """
        return '{0} {1}'.format(self.first_name, self.last_name)

    def display_skill(self) -> str:
        """Creates a string for the Skill.
        This is required to display genre in Admin.
        """
        return ', '.join([skill.name for skill in self.skill.all()])
    display_skill.short_description = 'Skill'


class SummaryMain(models.Model):
    """Model for Summary. Consists the main information about candidate's experience.
    """

    VISIBILITY_CHOICE = (
        ('v', 'Visible to anyone'),
        ('n', 'Not visible to anyone'),
    )

    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    salary = models.IntegerField()
    currency = models.CharField(
        max_length=1, choices=CURRENCY_CHOICE, default='r')
    visibility_status = models.CharField(
        max_length=1, choices=VISIBILITY_CHOICE, default='v')
    refresh_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self) -> HttpResponse:
        return reverse('summary_main', args=[str(self.id)])

    def __str__(self) -> str:
        return self.title


class SummaryDetail(models.Model):
    """Model for Summary. Consists the detailed information about candidate's experience.
    """

    MONTH_CHOICE = (
        ('00', ''),
        ('01', 'January'),
        ('02', 'Febraury'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    )

    summary = models.ForeignKey(SummaryMain, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=50)
    job_title = models.CharField(max_length=20)
    year_begin = models.CharField(max_length=4)
    month_begin = models.CharField(
        max_length=2, choices=MONTH_CHOICE, default='00')
    year_end = models.CharField(max_length=4)
    month_end = models.CharField(
        max_length=2, choices=MONTH_CHOICE, default='00')
    job_duty = models.TextField(max_length=500)

    def get_absolute_url(self) -> HttpResponse:
        return reverse('summary_detail', args=[str(self.id)])

    def __str__(self) -> str:
        return '{0}, {1} ({2}.{3})'.format(self.company_name,
                                           self.job_title,
                                           self.year_begin,
                                           self.month_begin)


class Employer(models.Model):
    """Model for Employees. Consists the main information about company.
    """

    company_name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    site = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    update_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self) -> HttpResponse:
        return reverse('employer', args=[str(self.id)])

    def __str__(self) -> str:
        return f'{self.company_name} ({self.site})'


class Vacancy(models.Model):
    """Model for Vacancy. Consists the main information about vacancy from Employer (Company).
    """

    company_name = models.ForeignKey(Employer, on_delete=models.CASCADE)
    vacancy_name = models.CharField(max_length=50)
    vacancy_description = models.TextField(max_length=200)
    key_skill = models.ManyToManyField(
        Technology, help_text='Select requiement(s) for vacancy')
    salary_min = models.IntegerField(blank=True, null=True)
    salary_max = models.IntegerField(blank=True, null=True)
    currency = models.CharField(
        max_length=1, choices=CURRENCY_CHOICE, default='r')
    publish_date = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def get_absolute_url(self) -> HttpResponse:
        return reverse('vacancy-detail', args=[str(self.id)])

    def __str__(self) -> str:
        return f'{self.vacancy_name} ({self.salary_min} - {self.salary_max})'

    def display_key_skill(self) -> str:
        """Creates a string for the Skill.
        This is required to display genre in Admin.
        """
        return ', '.join([skill.name for skill in self.key_skill.all()])
    display_key_skill.short_description = 'Skill'


class Profile(models.Model):
    """Model for user profile. Has connection with User-model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username


class Subscriber(models.Model):
    """Model for Subscriber. Class contains users for sending emails with news.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user.username}({self.user.email})'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created: bool, **kwargs) -> None:
    """If user profile created, it is auto-add into `common_users` group.
    """
    if created:
        group = Group.objects.get_or_create(name='common_users')
        instance.groups.add(group[0])


@receiver(user_signed_up)
def user_signed_up_(sender, request: HttpRequest, user, **kwargs) -> None:
    """Sending `Welcome email` after user sing-up into system.
    """
    subject, from_email, to = 'Welcome', 'admin@mysite', user.email
    text_content = "some custom text or html"
    html_content = ''
    msg = EmailMultiAlternatives(
        subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(post_save, sender=Vacancy)
def send_mail(sender, instance, created: bool, **kwargs) -> None:
    """Sending for all Subscribers `fresh` vacancy list.
    """
    if created:
        email_list = [s.user.email for s in Subscriber.objects.all()]
        subject = f'new vacancy created {instance.vacancy_name}'
        from_email = 'admin@mysite'
        text_content = 'Vacancy {0}, from company {1}'.format(
            instance.vacancy_name, instance.company_name)
        html_content = 'For more details go to <a href="{0}">link</a>.'.format(
            instance.get_absolute_url())
        msg = EmailMultiAlternatives(
            subject, text_content, from_email, email_list)
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class SMSLog(models.Model):
    """Store sended sms-codes.
    """

    phone_number = models.CharField(max_length=15)
    code = models.CharField(max_length=4, null=True, blank=True)
    server_response = models.TextField(max_length=200)
