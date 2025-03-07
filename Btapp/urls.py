from django.urls import path
from Btapp import views
from Btapp.views import AddComment, AddTicket, AddProject, ProjectDetailView

# Class-based views
from django.contrib.auth.decorators import login_required

# Para el sistema de autenticacion de django
from django.contrib.auth import views as auth_views

# Para MEDIA_URL
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.home, name='home'),

    # Tickets
    path('new_ticket/', AddTicket.as_view(), name='new_ticket'),
    path('ticket/index/', views.TicketIndexView.as_view(), name='ticket_index'),
    path('delete_ticket/<int:pk>', views.delete_ticket, name='delete_ticket'),
    path('ticket/<int:pk>/', login_required(views.TicketDetailView.as_view()), name='ticket_detail'),
    path('update_ticket/<int:pk>/', views.update_ticket, name='update_ticket'),

    # Projects
    path('new_project/', AddProject.as_view(), name='new_project'),
    path('project/index/', views.ProjectIndexView.as_view(), name='project_index'),
    path('project/<int:pk>/', ProjectDetailView.as_view(), name='project_detail'), 
    path('update_project/<int:pk>/', views.update_project, name='update_project'),

    # Comments
    path('ticket/<int:pk>/comment/', AddComment.as_view(), name='new_comment'), 

    # Users
    path('user/index/', views.UsersIndexView.as_view(), name='user_index'),

    # Authentication system
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),  # la carpeta account es necesaria
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='accounts/change_password.html'), name='password_change'),
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(template_name='accounts/change_password_done.html'), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/reset_password.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/reset_password_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/reset_password_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/reset_password_complete.html'), name='password_reset_complete'),
    path('sign_up/', views.sign, name='sign_up'), 
    
    # Dashboard
    path('accounts/profile/', views.profile, name='profile'), # A donde redirige la vista login 
    path('settings_profile/', views.setting_profile, name='settings_profile'),

    # Contact
    path('contact/', views.contact, name='contact'),
]

if settings.DEBUG: # Para que pueda mostrar el MEDIA_URL en deployment, no se recomienda para produccion
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
