from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory

# Create your models here.
CURRENCY_CHOICE = (
    ('r', 'RUB'),
    ('e', 'EUR'),
    ('u', 'USD'),
)


class Technology(models.Model):

    name = models.CharField(
        max_length=100, help_text='Enter a technology name')

    def __str__(self):
        return '{0}(id={1})'.format(self.name, self.id)


class Applicant(models.Model):

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

    def get_absolute_url(self):
        return reverse('applicant-detail', args=[str(self.id)])

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    def display_skill(self):
        """
        Creates a string for the Skill. This is required to display genre in Admin.
        """
        return ', '.join([skill.name for skill in self.skill.all()])
    display_skill.short_description = 'Skill'


class SummaryMain(models.Model):

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

    def get_absolute_url(self):
        return reverse('summary_main', args=[str(self.id)])

    def __str__(self):
        return self.title


class SummaryDetail(models.Model):

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

    def get_absolute_url(self):
        return reverse('summary_detail', args=[str(self.id)])

    def __str__(self):
        return '{0}, {1} ({2}.{3})'.format(self.company_name, self.job_title, self.year_begin, self.month_begin)


class Employer(models.Model):

    company_name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    site = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    update_date = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('employer', args=[str(self.id)])

    def __str__(self):
        return f'{self.company_name} ({self.site})'


class Vacancy(models.Model):

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

    def get_absolute_url(self):
        return reverse('vacancy', args=[str(self.id)])

    def __str__(self):
        return f'{self.vacancy_name} ({self.company_name})'

    def display_key_skill(self):
        """
        Creates a string for the Skill. This is required to display genre in Admin.
        """
        return ', '.join([skill.name for skill in self.key_skill.all()])
    display_key_skill.short_description = 'Skill'


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        default=1
    )

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.pk})


ProfileFormset = inlineformset_factory(User, Profile, fields=())
