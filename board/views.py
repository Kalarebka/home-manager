from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Board, Task, UserProfile
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, TaskForm
from django.utils import timezone


class IndexView(View):
    def get(self, request):
        context_dict = {}
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=request.user)
            context_dict['board_id'] = user_profile.board_id
        return render(request, "board/index.html", context=context_dict)


class AboutView(View):
    def get(self, request):
        return render(request, "board/about.html")


class ShowBoardView(View):

    def get(self, request):
        if request.user.is_authenticated:
            board = Board.objects.filter(id=request.user.board_id)
            context_dict = {}
            context_dict['title'] = board.name
            context_dict['board'] = board
            return render(request, 'board/show_board.html', context=context_dict)


class AddTaskView(View):

    def get(self, request):
        form = TaskForm()
        return render(request, "board/create_task.html", context={'form': form})

    def post(self, request):
        form = TaskForm(request.POST)
        new_task = Task.objects.create(form, commit=False)
        new_task.date_created = timezone.now()
        new_task.board = request.user.userprofile.board_id
        new_task.status = 'todo'
        new_task.save()
        return redirect(reverse('board:show_board'))


class CreateBoardView(View):
    pass


class UserProfileView(View):
    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        context_dict = {'profile': profile}
        render(request, 'board/user_profile.html', context=context_dict)


class EditTaskView(View):
    pass


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'board/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # If user does not have a board yet, the board_id is -1
            user_profile = UserProfile.objects.create(user=user, likes=0, board_id=None)
            user_profile.save()
            return redirect(reverse('board:index'))
        else:
            print(form.errors)
            return redirect(reverse('board:index'))



