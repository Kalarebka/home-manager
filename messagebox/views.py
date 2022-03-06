from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.core.exceptions import PermissionDenied

from .models import Message
from .forms import MessageForm


class MessagesView(View):
    def get(self, request):
        inbox = request.user.received_messages.order_by('-date')[:5]
        sent = request.user.sent_messages.order_by('-date')[:5]
        return render(request, 'messagebox/messages.html', context={'inbox': inbox, 'sent': sent})


class InboxView(View):
    def get(self, request):
        inbox = request.user.received_messages.order_by('-date')
        return render(request, 'messagebox/inbox.html', context={'inbox': inbox})


class SentView(View):
    def get(self, request):
        sent = request.user.sent_messages.order_by('-date')
        return render(request, 'messagebox/sent.html', context={'sent': sent})


class DeleteMessageView(View):
    pass


class NewMessageView(View):

    @method_decorator(login_required)
    def get(self, request):
        form = MessageForm()
        return render(request, 'messagebox/new_message.html', context={'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.from_user = request.user
            new_message.save()
            return redirect(reverse('messagebox:messages'))


class ShowMessageView(View):
    @method_decorator(login_required)
    def get(self, request, message_id):
        message = Message.objects.get(pk=message_id)
        if message.to_user == request.user or message.from_user == request.user:
            return render(request, 'messagebox/show_message.html', context={'message': message})
        else:
            raise PermissionDenied



