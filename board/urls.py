from django.urls import path

from . import views

app_name = "board"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('board/', views.DisplayBoardView.as_view(), name="display_board"),
    path('add_task/', views.AddTaskView.as_view(), name="add_task"),
    path('create_board/', views.CreateBoardView.as_view(), name="create_board"),
    path('user_profile/<int:user_id>', views.UserProfileView.as_view(), name='user_profile'),
    path('edit_task/', views.EditTaskView.as_view(), name='edit_task')
]