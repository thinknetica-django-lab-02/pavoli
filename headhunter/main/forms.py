from django import forms
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from .models import Profile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('user', 'birthday')

    user = forms.CharField(widget=forms.HiddenInput())
    birthday = forms.DateField(
        label='Age',
        widget=forms.DateInput(attrs={'class': 'form-control'})
    )


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )


ProfileFormset = inlineformset_factory(
    User, Profile, form=ProfileForm, can_delete=False, extra=0)
