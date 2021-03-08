from django.contrib import admin
from .models import Ticket, Project, Profile, Membership, Comment

# If you are happy with the default admin interface, you don’t need to define a ModelAdmin object at all (no tienes que definir estas clases)
class TicketAdmin(admin.ModelAdmin):
    date_hierarchy = 'opening_date'
    list_display = ['summary', 'author', 'project', 'opening_date', 'last_modified', 'stage']
    def close_ticket(self, request, queryset): # cambia el stage de un ticket
        queryset.update(stage=80)
    close_ticket.short_description = "Close selected tickets" # Para que sea human-readable
    actions = [close_ticket]

@admin.register(Project) # Puedes usar un decorador para hacer el registro de la clase
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'registration_date'] 
    ordering = ['registration_date']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'email']

@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ['person', 'project', 'date_joined']

    


# Register your models here
admin.site.register(Ticket, TicketAdmin) # La segunda entrada es solo si creaste una clase ModelAdmin
#admin.site.register(Project)
admin.site.register(Comment)
#admin.site.register(Membership)

