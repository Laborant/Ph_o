from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'class':'form-control'}), label='Email')
    password = forms.CharField(widget=PasswordInput(attrs={'class':'form-control'}), label='Пароль')


# class UserProfile(forms.Form):

