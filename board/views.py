from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Board, Task, UserProfile
from django.contrib.auth import authenticate, login, logout


class IndexView(View):
    def get(self, request):
        context_dict = {}
        return render("index.html", context=context_dict)


class DisplayBoardView(View):
    def get(self, request, board_id):
        board = Board.objects.filter(id=board_id)


class AddTaskView(View):
    pass


class CreateBoardView(View):
    pass


class UserProfileView(View):
    pass


class EditTaskView(View):
    pass


