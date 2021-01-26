from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

"La creamos"

urlpatterns = [
    path('login/' auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),

] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)