import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home_manager.settings")

import django

django.setup()

from board.models import Board, Task, UserProfile
from django.contrib.auth.models import User


def populate():
    users = [
        {"username": "ika", "password": "ikuwikuw"},
        {"username": "alu", "password": "aluwaluw"},
        {"username": "eryk", "password": "erykuwerykuw"},
    ]

    boards = [{""}]

    tasks = []

    for user in users:
        user_profile = add_user(user["username"], user["password"])


def add_user(username, password):
    user = User.objects.create(username=username)
    user.set_password(password)
    user.save()
    user_profile = UserProfile(user=user)
    user_profile.save()
    return user_profile


def add_board():
    pass


def add_task():
    pass


# Start execution here!
if __name__ == "__main__":
    print("Starting population script...")
    populate()
