from django import forms
from django.contrib.auth.models import User


class SignUpForm(forms.Form):
    name = forms.CharField(max_length=100)
    passwd = forms.CharField(widget=forms.PasswordInput)


class RecoveryPasswordForm(forms.Form):
    username = forms.CharField(max_length=100)
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
