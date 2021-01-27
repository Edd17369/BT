from django.contrib import admin
from .models import Ticket, Project


# If you are happy with the default admin interface, you don’t need to define a ModelAdmin object at all (no tienes que definir estas clases)
class TicketAdmin(admin.ModelAdmin):
    date_hierarchy = 'opening_date'
    list_display = ['description', 'author', 'project', 'opening_date']
    def close_ticket(self, request, queryset): # cambia el stage de un ticket
        queryset.update(stage=80)
    close_ticket.short_description = "Finish the ticket" # Para que sea human-readable

# Register your models here.
admin.site.register(Ticket, TicketAdmin) # La segunda entrada es solo si creaste una clase ModelAdmin



@admin.register(Project) # Si defines la clase puedes usar un decorador para hacer el registro
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['author']
    ordering = ['registration_date']

