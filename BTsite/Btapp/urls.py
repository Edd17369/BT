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

    # Authentication system
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),  # la carpeta account es necesaria
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/change_password.html'), name='password_change'),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/change_password_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/reset_password.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/reset_password_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/reset_password_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/reset_password_complete.html'), name='password_reset_complete'),
    path('accounts/profile/', views.home, name='profile'), # A donde redirige despues de login
    path('sign_up/', views.sign, name='sign_up'), 
    
    path('update_profile/', views.home, name='update_profile'),

]

if settings.DEBUG: # Para que pueda mostrar el MEDIA_URL en deployment, no se recomienda para produccion
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 