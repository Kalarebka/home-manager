from django import forms
from django.contrib.auth.models import User
from board.models import Board, UserProfile, Task
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    picture = forms.FileField()

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email', 'picture']
