from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core import validators
from django import forms
from .models import Photo


class Search(forms.Form):
    competention = 'Соревнование'
    bib_number = 'Стартовый номер'
    last_name = 'Фамилия'

class AddPhoto(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image', 'price', 'category', 'tag')

