from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Board(models.Model):
    name = models.CharField(max_length=128, unique=True)
    max_wip = models.IntegerField(default=5)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user


class Task(models.Model):
    HIGH = 'a'
    MEDIUM = 'b'
    LOW = 'c'
    priority_choices = [
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low')
    ]

    status_choices = [
        ('todo', 'To Do'),
        ('wip', 'In Progress'),
        ('done', 'Done')
    ]

    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    priority = models.CharField(choices=priority_choices, default=MEDIUM, blank=True, max_length=1)
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=1024, default='', blank=True)
    status = models.CharField(choices=status_choices, default='todo', max_length=4)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



