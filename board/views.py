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
        return render(request, "board/index.html", context=context_dict)


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
    pass


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
            # picture = request.FILES.picture
            user_profile = UserProfile.objects.create(user=user, likes=0,)
            user_profile.save()
            return redirect(reverse('board:index'))
        else:
            print(form.errors)
            return redirect(reverse('board:index'))



