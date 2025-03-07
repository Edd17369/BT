from django.db import models
from django.forms import ModelForm, widgets
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # one-to-one
    email = models.EmailField(max_length=100, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True) # null for the db and blank for the form validation
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    profile_pic = models.ImageField(default='img/user.jpg', blank=True, null=True, upload_to = 'img') # Para ImageField necesitas instalar Pillow

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user', 'email']
        widgets = {'first_name':widgets.TextInput(attrs={'class':'form-control'}),
                   'last_name':widgets.TextInput(attrs={'class':'form-control'}),
                   'phone':widgets.TextInput(attrs={'class':'form-control', 'placeholder':'Use the format ###-###-####'}),
                   'profile_pic':widgets.FileInput(attrs={'class':'form-control'}),
                   }
        labels = {'profile_pic': _('Profile Picture')}



class Project(models.Model):
    name = models.CharField(max_length=30) # unique, verbose_name
    members = models.ManyToManyField(User, through='Membership') # many-to-many
    registration_date = models.DateTimeField(auto_now_add=True)

    #def my_tickets(self): # No se necesita solo llama ObjProject.tickets.all() para obtener la lista
    #    list_of_tickets = Ticket.objects.filter(project=self)
    #    return list_of_tickets
    def has_open_tickets(self):
        my_tickets = Ticket.objects.filter(project=self).exclude(stage=80)
        return True if my_tickets else False
    def has_user(self, user):
        return user in self.members.all()

    # It’s important to add __str__() methods to your models, not only for your own convenience when dealing with the interactive
    # prompt, but also because objects’ representations are used throughout Django’s automatically-generated admin.
    def __str__(self): # returns a string representation of any object.
        return self.name

class ProjectForm(ModelForm):
    class Meta: # metadata is “anything that’s not a field”, such as table name or manager name or ordering
        model = Project
        fields = '__all__'
        widgets = {'registration_date':widgets.DateTimeInput(),
                   'members':widgets.SelectMultiple(attrs={'class':'form-control'}),
                   'name':widgets.TextInput(attrs={'class':'form-control'})}

class Membership(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='memberships', on_delete=models.CASCADE) # related_name the name to use for the relation from the related object back to this one.
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.person.__str__()



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

    author = models.ForeignKey(User, on_delete=models.CASCADE) # many-to-one
    project = models.ForeignKey(Project, related_name='tickets', on_delete=models.CASCADE)
    summary = models.CharField(max_length=100)
    level = models.CharField(max_length=2, choices=Levels.choices, default=Levels.Improvement)
    stage = models.CharField(max_length=2, choices=Stages.choices, default=Stages.Registered)  
    # The field is only automatically updated when calling Model.save().
    opening_date = models.DateTimeField(auto_now_add=True) # Automatically set the field to now when the object is first created.
    last_modified = models.DateTimeField(auto_now=True) # Automatically set the field to now every time the object is saved.
    description = models.TextField(max_length=500, null=True, blank=True)
    keywords = models.TextField(max_length=100, null=True, blank=True)
    attachments = models.FileField(blank=True, null=True, upload_to='uploads') # to specify a subdirectory of MEDIA_ROOT: MEDIA_ROOT/uploads

class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'  # to indicate that all fields in the model should be used.
        exclude = ['author'] # si quieres excluir un campo en el formulario
        widgets = {'opening_date':widgets.DateTimeInput(), # widgets: la forma en que se despliegan los campos del formulario
                   'last_modified':widgets.DateTimeInput(),
                   'summary':widgets.TextInput(attrs={'class':'form-control'}),
                   'description': widgets.Textarea(attrs={'rows': 4, 'class':'form-control'}),
                   'keywords': widgets.Textarea(attrs={'rows':2, 'class':'form-control'}), 
                   'author': widgets.Select(attrs={'disabled': True, 'class':'form-control'}),
                   'project':widgets.Select(attrs={'class':'form-control'}),
                   'stage':widgets.Select(attrs={'class':'form-control'}),
                   'level':widgets.Select(attrs={'class':'form-control'}),
                   'attachments':widgets.FileInput(attrs={'class':'form-control'}) # 'id':'customFile01', 'class':'custom-file-input', 'type':'file'
                   } 
        #labels = {'publication_date': _('Date'),
        #          'active': _('Status: Active')
        #          }


class Comment(models.Model):
    author = models.CharField(max_length=100, blank=True)
    ticket = models.ForeignKey(Ticket, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField(max_length=200)
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Ticket %s - %s' %(self.ticket.id, self.author)

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {'text':widgets.Textarea(attrs={'class':'form-control', 'rows':4}),}





