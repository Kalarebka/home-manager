from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from .models import Message
from .forms import MessageForm


class MessagesView(LoginRequiredMixin, View):
    def get(self, request):
        """Show five latest of received and sent messages."""
        inbox = request.user.received_messages.order_by("-date")[:5]
        sent = request.user.sent_messages.order_by("-date")[:5]
        return render(
            request, "messagebox/messages.html", context={"inbox": inbox, "sent": sent}
        )


class InboxView(LoginRequiredMixin, View):
    def get(self, request):
        """Show received messages (newest first)."""
        inbox = request.user.received_messages.order_by("-date")
        return render(request, "messagebox/inbox.html", context={"inbox": inbox})


class SentView(LoginRequiredMixin, View):
    def get(self, request):
        """Show sent messages (newest first)."""
        sent = request.user.sent_messages.order_by("-date")
        return render(request, "messagebox/sent.html", context={"sent": sent})


class DeleteMessageView(LoginRequiredMixin, View):
    """Delete message with specified id and redirect to previous page."""

    pass


class NewMessageView(LoginRequiredMixin, View):
    """Create and send a message to another user."""

    def get(self, request):
        form = MessageForm()
        return render(request, "messagebox/new_message.html", context={"form": form})

    def post(self, request):
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.from_user = request.user
            new_message.save()
            return redirect(reverse("messagebox:messages"))


class ShowMessageView(LoginRequiredMixin, View):
    def get(self, request, message_id):
        """Show message details."""
        message = Message.objects.get(pk=message_id)
        if message.to_user == request.user or message.from_user == request.user:
            return render(
                request, "messagebox/show_message.html", context={"message": message}
            )
        else:
            raise PermissionDenied
