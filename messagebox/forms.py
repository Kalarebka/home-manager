from django.contrib.auth.models import User
from .models import Message
from django.contrib.auth.models import User
from django.forms import ModelForm


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["to_user", "title", "text"]
