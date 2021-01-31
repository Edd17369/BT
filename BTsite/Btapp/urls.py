from django.urls import path
from . import views

# Para el sistema de autenticacion de django
from django.contrib.auth import views as auth_views

# Para MEDIA_URL
from django.conf import settings
from django.conf.urls.static import static

"La creamos"

urlpatterns = [
    path('', views.home, name='home'),

    # Tickets y Proyectos
    path('new_ticket/', views.new_ticket, name='new_ticket'),
    path('new_project/', views.new_project, name='new_project'),

    path('ticket/index/', views.TicketIndexView.as_view(), name='ticket_index'),
    path('ticket/<int:pk>/', views.TicketDetailView.as_view(), name='ticket_detail'),
    #path('ticket/index/', views.ticket_index, name='tickets'), # Ya no se usan uso los de arriba
    #path('ticket/<int:id>/', views.ticket_detail, name='ticket_id'),

    path('project/index/', views.ProjectIndexView.as_view(), name='project_index'),
    path('project/<int:id>/', views.project_detail, name='project_detail'),

    #path('login/' auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),

] #+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)