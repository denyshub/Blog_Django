from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        user = get_user_model()
        fields = ['username', 'password']

class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='Логін',  widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password_check = forms.CharField(label='Пароль', widget=forms.PasswordInput())

    class Meta:
        model =get_user_model()
        fields = ['username', 'email', 'first_name','last_name','password', 'password_check']
        labels = {'email': 'email', 'first_name': 'Ім\'я', 'last_name':'Прізвище'}

