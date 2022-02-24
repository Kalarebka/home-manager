from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Board, Task, UserProfile
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm, TaskForm, BoardForm
from django.utils import timezone
from collections import namedtuple


class IndexView(View):
    def get(self, request):
        context_dict = {}
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=request.user)
            context_dict['board_id'] = user_profile.board
        return render(request, "board/index.html", context=context_dict)


class AboutView(View):
    def get(self, request):
        return render(request, "board/about.html")


class ShowBoardView(View):

    @method_decorator(login_required)
    def get(self, request):
        board = request.user.userprofile.board
        context_dict = {}
        if board:
            context_dict['title'] = board.name
            context_dict['max_wip'] = board.max_wip
            context_dict['tasks'] = get_tasks_by_status(board)
            context_dict['current_wip'] = len(context_dict['tasks'].in_progress)
        else:
            redirect(reverse('board:create_board'))
        return render(request, 'board/show_board.html', context=context_dict)


class AddTaskView(View):

    @method_decorator(login_required)
    def get(self, request):
        form = TaskForm()
        return render(request, "board/create_task.html", context={'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.date_created = timezone.now()
            new_task.status = 'todo'
            new_task.board = request.user.userprofile.board
            if not new_task.board:
                return redirect(reverse('board:add_task_fail'))
            new_task.save()
            return redirect(reverse('board:add_task_success'))
        else:
            return redirect('board:add_task_fail', context={'message': 'Something went wrong when adding the task'})


class AddTaskSuccessView(View):
    def get(self, request):
        return render(request, 'board/add_task_success.html')


class AddTaskFailView(View):
    def get(self, request):
        return render(request, 'board/add_task_fail.html')


class CreateBoardView(View):

    @method_decorator(login_required)
    def get(self, request):
        form = BoardForm()
        return render(request, "board/create_board.html", context={'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = BoardForm(request.POST)
        if form.is_valid():
            new_board = form.save(commit=False)
            new_board.created_by = request.user
            new_board.save()
            profile = request.user.userprofile
            profile.board_id = new_board.id
            profile.save()
            return redirect(reverse('board:index'))
        else:
            redirect('board:add_task_fail', {'message': 'Something went wrong when adding the board'})


class UserProfileView(View):

    @method_decorator(login_required)
    def get(self, request):
        profile = request.user.userprofile
        context_dict = {'profile': profile}
        return render(request, 'board/user_profile.html', context=context_dict)


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


# Helper functions

def get_tasks_by_status(board: Board) -> namedtuple:
    todo = Task.objects.filter(board=board.id, status='todo').order_by('priority', '-date_created')
    in_progress = Task.objects.filter(board=board.id, status='wip')
    done = Task.objects.filter(board=board.id, status='done').order_by('-date_completed')
    TaskData = namedtuple("TaskData", "todo in_progress done")
    data = TaskData(todo=todo, in_progress=in_progress, done=done)
    return data


