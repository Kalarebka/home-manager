from django.db import models
from django.utils import timezone


class Board(models.Model):
    name = models.CharField(max_length=128, unique=True)


class UserProfile(models.Model):
    picture = models.FileField()


class Task(models.Model):
    board = models.ForeignKey(Board)
    created_by = models.ForeignKey(User)
    assigned_to = models.ForeignKey(User)
    priority = models.IntegerChoices()

