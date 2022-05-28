from collections import namedtuple

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.decorators.http import require_http_methods

from messagebox.models import Message

from .forms import RegisterForm, TaskForm, BoardForm
from .models import Board, Task, UserProfile


class IndexView(View):
    def get(self, request):
        # TODO
        """ If user is not logged in, display basic info about the page and sample pictures.
        If user is logged in, display welcome message and overview of user's activity and tasks. """
        context_dict = {}
        if request.user.is_authenticated:
            user_profile = UserProfile.objects.get(user=request.user)
            context_dict['board_id'] = user_profile.board
        return render(request, "board/index.html", context=context_dict)


class AboutView(View):
    def get(self, request):
        """ Display description of the page. """
        return render(request, "board/about.html")


class ShowBoardView(LoginRequiredMixin, View):
    def get(self, request):
        """ Display user's board. If no board, display links to create or join one. """
        board = request.user.userprofile.board
        context_dict = {}
        if board:
            context_dict['board'] = board
            context_dict['tasks'] = get_tasks_by_status(board)
            context_dict['current_wip'] = len(context_dict['tasks'].wip)
        else:
            context_dict['board'] = None
        return render(request, 'board/show_board.html', context=context_dict)


class AddTaskView(LoginRequiredMixin, View):
    """ Add task to user board"""
    def get(self, request):
        board = request.user.userprofile.board
        if not board:
            return redirect(reverse('board:show_board'))
        form = TaskForm()
        return render(request, "board/create_task.html", context={'form': form})

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


class CreateBoardView(LoginRequiredMixin, View):
    """ Create a board for currently logged in user"""
    def get(self, request):
        form = BoardForm()
        return render(request, "board/create_board.html", context={'form': form})

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


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request, pk):
        """ Display user profile. """
        context_dict = {'profile': get_user_profile(pk)}
        return render(request, 'board/user_profile.html', context=context_dict)

    def post(self, request, pk):
        # TODO
        """ Update profile picture. Show only on currently logged in user's profile. """
        profile = get_user_profile(pk)
        profile.picture = request.FILES.get("profile_picture")
        # Rename the profile picture to user's name
        # profile.picture.name = profile.picture.name.split(".")
        profile.save()
        context_dict = {'profile': profile}
        return render(request, 'board/user_profile.html', context_dict)


class MarkCompletedView(LoginRequiredMixin, View):
    def get(self, request, task_id):
        board = request.user.userprofile.board
        board.current_wip -= 1
        task = Task.objects.get(pk=task_id)
        task.status = 'done'
        task.save()
        board.save()
        return redirect(reverse('board:show_board'))


class ResignTaskView(LoginRequiredMixin, View):
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
            # Automatically login the newly registered user
            user_to_log = authenticate(request, username=form.cleaned_data['username'],
                                       password=form.cleaned_data['password1'],
                                       )
            login(request, user_to_log)
            return redirect(reverse('board:index'))
        else:
            messages.warning(request, 'Please correct the error below.')
            return render(request, 'board/register.html', {'form': form})


class UserListView(LoginRequiredMixin, View):
    def get(self, request):
        users = User.objects.exclude(username=request.user.username)
        return render(request, 'board/user_list.html', context={'users': users})


class AssignTaskView(LoginRequiredMixin, View):
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


class JoinBoardView(LoginRequiredMixin, View):
    def get(self, request):
        boards = Board.objects.all()
        boards_with_creators = []
        for board in boards:
            creator = board.created_by
            boards_with_creators.append((board, creator))
        return render(request, 'board/join_board.html', context={'boards': boards_with_creators})
    def post(self, request, board):
        board_creator = board.created_by
        send_message(request.user.id, board_creator.id, "placeholder")

# Helper functions

def prepare_tasks_data(user):
    """ Prepare context dictionary for rendering tasks on the board."""
    profile = get_user_profile(user.pk)
    data = {}
    data['board'] = profile.board
    data['tasks'] = get_tasks_by_status(data['board'])
    data['current_wip'] = len(data['tasks'].wip)
    return data

def get_user_profile(pk):
    user = User.objects.get(pk=pk)
    profile = user.userprofile
    return profile


def get_tasks_by_status(board: Board) -> namedtuple:
    todo = Task.objects.filter(board=board.id, status='todo').order_by('priority', '-date_created')
    wip = Task.objects.filter(board=board.id, status='wip')
    done = Task.objects.filter(board=board.id, status='done').order_by('-date_completed')
    TaskData = namedtuple("TaskData", "todo wip done")
    data = TaskData(todo=todo, wip=wip, done=done)
    return data

# TODO (for sending automated messages)
def send_message(from_user, to_user, title='untitled', message='', ):
    message = Message.objects.create(from_user=from_user, to_user=to_user, title=title, message=message)



# Function views for HTMX


@require_http_methods(['DELETE'])
def delete_task(request, pk):
    Task.objects.filter(pk=pk).delete()
    context_dict = prepare_tasks_data(request.user)
    return render(request, 'partials/tasks.html', context=context_dict)

@require_http_methods(['GET', 'POST'])
def edit_task(request, pk):
    if request.method == "GET":
        task = Task.objects.get(pk=pk)
        form = TaskForm(instance=task)
        context_dict = {'form': form, 'instance': task}
        return render(request, 'board/edit_task.html', context_dict)
    else:
        task = Task.objects.get(pk=pk)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return HttpResponse(status=204)


def assign_task(request, pk):
    task = Task.objects.filter(pk=pk).first()
    task.assigned_to = request.user
    task.status = 'wip'
    task.save()
    context_dict = prepare_tasks_data(request.user)
    return render(request, 'partials/tasks.html', context=context_dict)


def resign_task():
    return None


def complete_task(request, pk):
    task = Task.objects.filter(pk=pk).first()
    task.status = 'done'
    task.save()
    context_dict = prepare_tasks_data(request.user)
    return render(request, 'partials/tasks.html', context=context_dict)
