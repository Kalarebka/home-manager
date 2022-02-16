"""home_manager URL Configuration
"""
from django.contrib import admin
from django.urls import include, path
from board.views import IndexView

urlpatterns = [
    path('', IndexView.as_view()),
    path('board/', include('board.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
