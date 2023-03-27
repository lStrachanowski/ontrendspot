import email

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

class ResetEmail(forms.Form):
    email = forms.EmailField(max_length=254)

class ResetForm(forms.Form):
    password = forms.CharField(max_length=254)
    confirm_password = forms.CharField(max_length=254)
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise ValidationError("Passwords don`t match!")


class FieldCheck(forms.Form):
    new_name = forms.CharField(max_length=30)

class EmailCheck(forms.Form):
    new_email = forms.EmailField(max_length=254)

class ChangePassword(forms.Form):
    oldPass = forms.CharField(widget=forms.PasswordInput)
    newPass = forms.CharField(widget=forms.PasswordInput)
    confirmNewPass = forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super().clean()
        oldPassword = cleaned_data.get("oldPass")
        newPassword = cleaned_data.get("newPass")
        confirmNewPass = cleaned_data.get("confirmNewPass")
        if newPassword != confirmNewPass:
            raise ValidationError("Passwords don`t match")
