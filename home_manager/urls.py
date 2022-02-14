"""home_manager URL Configuration
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('board/', include('board.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
]
