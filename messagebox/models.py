from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_messages"
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_messages"
    )
    title = models.CharField(max_length=128, default="Untitled")
    text = models.TextField()
    date = models.DateField(auto_now=True)
    read_status = models.BooleanField(default=False)
