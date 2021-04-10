from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory

from main.models import (
    Profile,
    Vacancy, Employer,
)


class ProfileForm(forms.ModelForm):
    user = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'user')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)


ProfileFormSet = inlineformset_factory(User, Profile, fields=(
    'date_of_birth',), extra=0, min_num=1, can_delete=False)


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = '__all__'


vacancy_formset = inlineformset_factory(
    Employer, Vacancy, fields=('vacancy_name', 'vacancy_description', 'key_skill', 'salary_min', 'salary_max', 'currency'), extra=1)
