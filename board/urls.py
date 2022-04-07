from django.urls import path

from . import views

app_name = "board"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('show_board/', views.ShowBoardView.as_view(), name="show_board"),
    path('add_task/', views.AddTaskView.as_view(), name="add_task"),
    path('create_board/', views.CreateBoardView.as_view(), name="create_board"),
    path('user_profile/<int:pk>/', views.UserProfileView.as_view(), name='user_profile'),
    # path('edit_task/<int:task_id>/', views.EditTaskView.as_view(), name='edit_task'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('add_task_success/', views.AddTaskSuccessView.as_view(), name='add_task_success'),
    path('add_task_fail/', views.AddTaskFailView.as_view(), name='add_task_fail'),
    path('user_list/', views.UserListView.as_view(), name='user_list'),
    # path('assign_task/<int:task_id>/', views.AssignTaskView.as_view(), name='assign_task'),
    path('mark_completed/<int:task_id>/', views.MarkCompletedView.as_view(), name='mark_completed'),
    path('resign_task/<int:task_id>', views.ResignTaskView.as_view(), name='resign_task'),
    path('join_board', views.JoinBoardView.as_view(), name='join_board'),
]

htmx_views = [
    path('tasks/<int:pk>/delete', views.delete_task, name='delete_task'),
    path('tasks/<int:pk>/edit', views.edit_task, name="edit_task"),
    path('tasks/<int:pk>/assign', views.assign_task, name="assign_task"),
    path('tasks/<int:pk>/resign', views.resign_task, name="resign_task"),
    path('tasks/<int:pk>/complete', views.complete_task, name="complete_task"),
]

urlpatterns += htmx_views
