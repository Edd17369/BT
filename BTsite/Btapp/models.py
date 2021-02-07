from django.db import models
from django.forms import ModelForm,widgets
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User

# Create your models here.


class Project(models.Model):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def my_tickets(self):
        list_of_tickets = Ticket.objects.filter(project=self)
        return list_of_tickets
    def has_open_tickets(self):
        my_tickets = Ticket.objects.filter(project=self)
        for t in my_tickets:
            if t.stage != '80':
                return True
        return False


    # It’s important to add __str__() methods to your models, not only for your own convenience when dealing with the interactive
    # prompt, but also because objects’ representations are used throughout Django’s automatically-generated admin.
    def __str__(self):
        return self.title

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {'registration_date':widgets.DateTimeInput(), 
                   'author': widgets.Select(attrs={'disabled': True}),}



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
        #Accepted = 40, _('Accepted')
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
    comments = models.TextField(max_length=1000, null=True, blank=True)
    attachments = models.FileField(blank=True, null=True, upload_to='uploads') # to specify a subdirectory of MEDIA_ROOT: MEDIA_ROOT/uploads

class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'  # to indicate that all fields in the model should be used.
        #exclude = ['stage'] # si quieres excluir un campo en el formulario
        widgets = {'opening_date':widgets.DateTimeInput(), # widgets: la forma en que se despliegan los campos del formulario
                   'last_modified':widgets.DateTimeInput(),
                   'description': widgets.Textarea(attrs={'rows': 5}),
                   'keywords': widgets.Textarea(attrs={'rows':2}), 
                   'author': widgets.Select(attrs={'disabled': True}),} # ,'attachment':widgets.ClearableFileInput(attrs={'multiple':True}) 
        #labels = {'publication_date': _('Date'),
        #          'active': _('Status: Active')
        #          }



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, help_text="Use the format ###-###-####", null=True, blank=True)
    profile_pic = models.ImageField(default='img/user.jpg', blank=True, null=True, upload_to = 'img') # Para ImageField necesitas instalar Pillow

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user', 'email']
        labels = {'profile_pic': _('Profile Picture')}
