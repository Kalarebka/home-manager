from django import forms
from django.contrib.auth.models import User
from board.models import Board, UserProfile, Task
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']


class TaskForm(ModelForm):
    pass


class BoardForm(ModelForm):
    pass
