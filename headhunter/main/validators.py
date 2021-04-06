from datetime import date, datetime
from django.forms import ValidationError


def validator_age(value):
    today = date.today()
    date_check = datetime.strptime(
        f"{today.year - 18}{today.month}{today.day}", '%Y%m%d').date()

    if date_check < value:
        raise ValidationError('Возраст меньше 18 лет!')

    return value
