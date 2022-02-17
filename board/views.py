from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Board, Task, UserProfile
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm


class IndexView(View):
    def get(self, request):
        context_dict = {}
        profile = UserProfile.objects.get(user=request.user.id)
        context_dict['profile'] = profile
        return render(request, "board/index.html", context=context_dict)


class AboutView(View):
    def get(self, request):
        return render(request, "board/about.html")


class ShowBoardView(View):
    def get(self, request, board_id):
        board = Board.objects.filter(id=board_id)
        context_dict = {}
        context_dict['title'] = board.name
        return render(request, 'board/show_board.html', context=context_dict)


class AddTaskView(View):
    pass


class CreateBoardView(View):
    pass


class UserProfileView(View):
    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)
        render(request, 'board/user_profile.html')


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
            user_profile = UserProfile.objects.create(user=user, likes=0, board_id=-1)
            user_profile.save()
            return redirect(reverse('board:index'))
        else:
            print(form.errors)
            return redirect(reverse('board:index'))



