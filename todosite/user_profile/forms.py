from django import forms


class ChangeUserName(forms.Form):
    new_name = forms.CharField(max_length=15)
