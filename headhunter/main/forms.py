from datetime import datetime

from django import forms
from django.contrib.auth.models import User

from .models import Profile


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('birthday',)

    def __init__(self, *args, user, **kwargs):
        self.fields['birthday'] = forms.DateField(
            widget=forms.SelectDateWidget(), label='Birthdate')


class ProfileFormset (forms.inlineformset_factory(User, Profile, fields=('birthday',), can_delete=False)):
    def __init__(self, *args, **kwargs):
        self.__initial = kwargs.pop('initial', [])
        super().__init__(*args, **kwargs)

    def clean(self):
        super().clean()

        for form in self.forms:
            data = form.cleaned_data['birthday']
            birth_date_delta = datetime.now().date().year - data.year
            if birth_date_delta < 18:
                form.add_error('birthday', 'Only from 18 y.o.')
                raise forms.ValidationError('Access denied!')
            return data
