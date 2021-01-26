from django.db import models
from django.forms import ModelForm,widgets
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User

# Create your models here.

# Objectivo: registrar las bases de datos.

# La base de datos de un BTS debe registrar los hechos e historia de un fallo de software. 
# Los hechos pueden ser una descripcion detallada del fallo, la severidad del evento, forma de reproducirlo, 
# los usuarios involucrados en la solución así como fecha probable de solucion y codigo que corrige el 
# problema o posibles soluciones. 

# La base de datos se debe de rellenar con un formulario
# la primera vez que corras el server hay que hacer antes las migraciones
# cada que modifiques los campos del modelo hay que hacer las migraciones (cosas de estilo no)
# registra el modelo en el admin.py


class Project(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def number_of_tickets(self):
        list_reports = Ticket.objects.filter(project=self)
        return len(list_reports)

    def __str__(self):
        return self.title


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {'author': widgets.Select(attrs={'disabled': True}),
                   'registration_date':widgets.DateTimeInput()}



class Ticket(models.Model): 
    class Levels(models.TextChoices):   # tienen la propiedad .label que da el nombre
        Improvement = 10, _('Improvement') # primera entrada: valor en el modelo, segunda entreda: human-readable
        Trivial = 20, _('Trivial')
        Less = 30, _('Less')
        Normal = 50, _('Normal')
        Major = 70, _('Major')
        Critical = 90, _('Critical')
    class Stages(models.TextChoices):
        Registered = 20, _('Registered')
        Accepted = 40, _('Accepted')
        Working_On = 60, _('Working on')
        Closed = 80, _('Closed')

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    #users_involved = models.CharField(max_length=30, null=True, blank=True)
    level = models.CharField(max_length=2, choices=Levels.choices, default=Levels.Improvement)
    stage = models.CharField(max_length=2, choices=Stages.choices, default=Stages.Registered)  
    
    # The field is only automatically updated when calling Model.save().
    opening_date = models.DateTimeField(auto_now_add=True) # Automatically set the field to now when the object is first created.
    last_modified = models.DateTimeField(auto_now=True) # Automatically set the field to now every time the object is saved.

    description = models.TextField(max_length=500)
    keywords = models.TextField(max_length=100, null=True, blank=True)
    comments = models.TextField(max_length=200, null=True, blank=True)
    attachments = models.FileField(blank=True, null=True, upload_to='uploads') # to specify a subdirectory of MEDIA_ROOT: MEDIA_ROOT/uploads


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'  # to indicate that all fields in the model should be used.
        #exclude = ['active', 'duration', 'solution'] # si quieres excluir un campo en el formulario
        widgets = {'author': widgets.Select(attrs={'disabled': True}), # widgets: la forma en que se despliegan los campos del formulario
                   'opening_date':widgets.DateTimeInput(),
                   'last_modified':widgets.DateTimeInput(),
                   'description': widgets.Textarea(attrs={'rows': 4}),
                   } # ,'attachment':widgets.ClearableFileInput(attrs={'multiple':True}) 
        #labels = {'publication_date': _('Date'),
        #          'active': _('Status: Active')
        #          }