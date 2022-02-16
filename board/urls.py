from django.urls import path

from . import views

app_name = "board"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('show_board/', views.ShowBoardView.as_view(), name="show_board"),
    path('add_task/', views.AddTaskView.as_view(), name="add_task"),
    path('create_board/', views.CreateBoardView.as_view(), name="create_board"),
    path('user_profile/<int:user_id>', views.UserProfileView.as_view(), name='user_profile'),
    path('edit_task/', views.EditTaskView.as_view(), name='edit_task'),
    path('register/', views.RegisterView.as_view(), name='register')
]