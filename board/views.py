from collections import namedtuple

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View

from .forms import RegisterForm, TaskForm, BoardForm
from .models import Board, Task, UserProfile


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
            context_dict['current_wip'] = len(context_dict['tasks'].wip)
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
    def get(self, request, username):
        user = User.objects.get(username=username)
        profile = user.userprofile
        context_dict = {'profile': profile}
        return render(request, 'board/user_profile.html', context=context_dict)


class EditTaskView(View):

    def get(self, request, task_id):
        task = Task.objects.get(pk=task_id)
        form = TaskForm(instance=task)
        context_dict = {'form': form, 'instance': task}
        return render(request, 'edit_task.html', context_dict)

    def post(self, request, task_id):
        task = Task.objects.get(pk=task_id)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect(reverse('board:show_board'))


class MarkCompletedView(View):
    @method_decorator(login_required)
    def get(self, request, task_id):
        board = request.user.userprofile.board
        board.current_wip -= 1
        task = Task.objects.get(pk=task_id)
        task.status = 'done'
        task.save()
        board.save()
        return redirect(reverse('board:show_board'))


class ResignTaskView(View):
    @method_decorator(login_required)
    def get(self, request, task_id):
        board = request.user.userprofile.board
        board.current_wip -= 1
        task = Task.objects.get(pk=task_id)
        task.status = 'todo'
        task.assigned_to = None
        task.save()
        board.save()
        return redirect(reverse('board:show_board'))


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'board/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile.objects.create(user=user, likes=0, board_id=None)
            user_profile.save()
            user_to_log = authenticate(request, username=form.cleaned_data['username'],
                                       password=form.cleaned_data['password1'],
                                       )
            login(request, user_to_log)
            return redirect(reverse('board:index'))
        else:
            print(form.errors)
            return render(request, 'board/register.html', {'form': form})


class UserListView(View):
    @method_decorator(login_required)
    def get(self, request):
        users = User.objects.exclude(username=request.user.username)
        return render(request, 'board/user_list.html', context={'users': users})


class AssignTaskView(View):
    @method_decorator(login_required)
    def get(self, request, task_id):
        board = request.user.userprofile.board
        if board.current_wip < board.max_wip:
            task = Task.objects.get(pk=task_id)
            task.assigned_to = request.user
            task.status = 'wip'
            task.save()
            board.current_wip += 1
            board.save()
            return redirect(reverse('board:show_board'))

# Helper functions


def get_tasks_by_status(board: Board) -> namedtuple:
    todo = Task.objects.filter(board=board.id, status='todo').order_by('priority', '-date_created')
    wip = Task.objects.filter(board=board.id, status='wip')
    done = Task.objects.filter(board=board.id, status='done').order_by('-date_completed')
    TaskData = namedtuple("TaskData", "todo wip done")
    data = TaskData(todo=todo, wip=wip, done=done)
    return data


