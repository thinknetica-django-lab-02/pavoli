from django.db import models
from django.urls import reverse

# Create your models here.


class Applicant(models.Model):

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20)

    GENDER_CHOICE = (
        ('m', 'male'),
        ('f', 'female'),
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICE, blank=True)
    # cv = models.ManyToManyField('SummaryMain')

    def get_absolute_url(self):
        return reverse('person', args=[str(self.id)])

    def __str__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)


class SummaryMain(models.Model):

    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    salary = models.IntegerField()

    CURRENCY_CHOICE = (
        ('r', 'RUB'),
        ('e', 'EUR'),
        ('u', 'USD'),
    )

    currency = models.CharField(
        max_length=1, choices=CURRENCY_CHOICE, default='r')

    VISIBILITY_CHOICE = (
        ('v', 'Visible to anyone'),
        ('n', 'Not visible to anyone'),
    )

    visibility_status = models.CharField(
        max_length=1, choices=VISIBILITY_CHOICE, default='v')

    refresh_date = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('cv_head', args=[str(self.id)])

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

    def __str__(self):
        return '{0}, {1} ({2}.{3})'.format(self.company_name, self.job_title, self.year_begin, self.month_begin)
