"""home_manager URL Configuration
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

# from django_registration.backends.one_step.views import RegistrationView

urlpatterns = [
    path("", include("board.urls")),
    path("admin/", admin.site.urls),
    # path('accounts/', include('django_registration.backends.one_step.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
    path("messagebox/", include("messagebox.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
