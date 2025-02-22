from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from task_manager.users.models import User

class UserUpdateForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Имя'
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Фамилия'
    )
    username = forms.CharField(
        max_length=30,
        required=True,
        label='Имя пользователя'
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user
