from django.urls import path

from . import views

app_name = "messagebox"
urlpatterns = [
    path('', views.MessagesView.as_view(), name='messages'),
    path('inbox/', views.InboxView.as_view(), name='inbox'),
    path('sent/', views.SentView.as_view(), name='sent'),
    path('delete_message/<int:id>/', views.DeleteMessageView.as_view(), name='delete_message'),
    path('new_message/', views.NewMessageView.as_view(), name='new_message'),
    path('show_message/<int:id>', views.ShowMessageView.as_view(), name='show_message'),
]