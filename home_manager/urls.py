"""home_manager URL Configuration
"""
from django.contrib import admin
from django.urls import include, path
# from django_registration.backends.one_step.views import RegistrationView

urlpatterns = [
    path('', include('board.urls')),
    path('admin/', admin.site.urls),
    # path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
