from django.urls import path
from . import views

# Para el sistema de autenticacion de django
from django.contrib.auth import views as auth_views

# Para MEDIA_URL
from django.conf import settings
from django.conf.urls.static import static

"La creamos"

urlpatterns = [
    #path('', views.index, name='home'),
    path('new_ticket/', views.new_ticket, name='new_ticket'),
    path('new_project/', views.new_project, name='new_project'),
    #path('login/' auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),

] #+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)