from django.contrib.auth.models import User
from board.models import Board, Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "priority"]


class BoardForm(ModelForm):
    class Meta:
        model = Board
        fields = ["name", "max_wip", "access_code"]
