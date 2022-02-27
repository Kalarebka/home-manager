from django.contrib.auth.models import User
from django.db import models


class Board(models.Model):
    name = models.CharField(max_length=128)
    max_wip = models.IntegerField(default=5)
    current_wip = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    access_code = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(default='default.jpg', upload_to='profile_images', blank=True, null=True)
    likes = models.IntegerField(default=0)
    board = models.ForeignKey(Board, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username


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

    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    priority = models.CharField(choices=priority_choices, default=MEDIUM, blank=True, max_length=1)
    title = models.CharField(max_length=256)
    description = models.TextField(max_length=1024, default='', blank=True)
    status = models.CharField(choices=status_choices, default='todo', max_length=4)
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title



