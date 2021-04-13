from django import forms
from django.contrib.auth.models import User
from django.forms.models import inlineformset_factory
from allauth.account.forms import LoginForm
from django.contrib.auth.forms import UserCreationForm

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


class VacancyAddForm(forms.ModelForm):

    class Meta:
        model = Vacancy
        fields = ['company_name', 'vacancy_name', 'vacancy_description',
                  'key_skill', 'salary_min', 'salary_max', 'currency']


class VacancyUpdateForm(forms.ModelForm):

    class Meta:
        model = Vacancy
        fields = ['company_name', 'vacancy_name', 'vacancy_description',
                  'key_skill', 'salary_min', 'salary_max', 'currency']


class CreateNewUser(UserCreationForm):

    username = forms.CharField(
        label='Login', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(
        label='Password1', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Password2', widget=forms.PasswordInput(
        attrs={'class': 'form-input'}))
    email = forms.EmailField(
        label='Email', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email')
