from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.Form):
    name = forms.CharField(max_length=100)
    passwd = forms.CharField(widget=forms.PasswordInput)
