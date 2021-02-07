from django.contrib import admin
from .models import Ticket, Project, Profile

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# If you are happy with the default admin interface, you don’t need to define a ModelAdmin object at all (no tienes que definir estas clases)
class TicketAdmin(admin.ModelAdmin):
    date_hierarchy = 'opening_date'
    list_display = ['description', 'author', 'project', 'opening_date', 'last_modified']
    def close_ticket(self, request, queryset): # cambia el stage de un ticket
        queryset.update(stage=80)
    close_ticket.short_description = "Finish the ticket" # Para que sea human-readable

@admin.register(Project) # Puedes usar un decorador para hacer el registro de la clase
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['author', 'registration_date']
    ordering = ['registration_date']

# Define an inline admin descriptor for Profile model which acts a bit like a singleton
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']
    #ordering = ['name']


# Register your models here
admin.site.register(Ticket, TicketAdmin) # La segunda entrada es solo si creaste una clase ModelAdmin
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
