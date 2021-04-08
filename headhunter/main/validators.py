from django.forms import ValidationError
from dateutil.relativedelta import relativedelta
from django.utils import timezone


def validate_age(value):
    age = relativedelta(timezone.now().date(), value).years

    if age < 18:
        raise ValidationError('Возраст меньше 18 лет!')
