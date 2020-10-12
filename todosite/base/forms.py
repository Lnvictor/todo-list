from django import forms
from .models import status_choices
from django.contrib.auth.models import User


class SignUpForm(forms.Form):
    name = forms.CharField(label="Seu Nome", max_length=100)
    passwd = forms.CharField(widget=forms.PasswordInput)


class NewTaskForm(forms.Form):
    task_name = forms.CharField(max_length=30)
    description = forms.CharField(max_length=120)
    pub_date = forms.DateField()
    status = forms.ChoiceField(choices=status_choices)


class NewIssueForm(forms.Form):
    description = forms.CharField(max_length=120)
    pub_date = forms.DateField()
    status = forms.ChoiceField(choices=status_choices)
