import email
from click import password_option
from django import forms
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    user = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError("Passwords don`t match!")
        

class ResetForm(forms.Form):
    email = forms.EmailField(max_length=254)