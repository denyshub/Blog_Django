from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        user = get_user_model()
        fields = ['username', 'password']



class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput())
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(), required=True)
    password2 = forms.CharField(label='Підтвердити пароль', widget=forms.PasswordInput(), required=True)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        exclude = ['password_auth',]
        labels = {
            'email': 'Email',
            'first_name': 'Ім\'я',
            'last_name': 'Прізвище'
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Email вже зареєстрований')
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логін', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(disabled=True, label='Email', widget=forms.TextInput(attrs={'class': 'form-input'}))

    class Meta:

        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {
            'email': 'Email',
            'first_name': 'Ім\'я',
            'last_name': 'Прізвище'
        }

