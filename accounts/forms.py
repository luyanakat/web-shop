from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'phone_number', 'email', 'password']
