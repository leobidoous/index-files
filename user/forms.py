# coding=utf-8
from django.contrib.auth.forms import UserCreationForm

from user.models import UserModel
from django import forms


class UserAdminCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password']


class UserForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ['username', 'email', 'password']

