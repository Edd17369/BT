from django.shortcuts import render, redirect, HttpResponse, get_object_or_404

from .models import Ticket, TicketForm, Project, ProjectForm
from django.contrib.auth.models import User

# Forms
from .forms import SignForm

# Authentication
from django.contrib.auth.decorators import login_required
from django.contrib.auth import  login
from django.contrib.auth.password_validation import validate_password, password_validators_help_text_html
from django.conf import  settings
from django.core.mail import send_mail

from django.contrib import messages

from django.views import generic # vistas genericas



### HOME
def home(request):
    return render(request, "Btapp/home.html")


### TICKETS
@login_required # The view code is free to assume the user is logged in
def new_ticket(request):
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        request.POST._mutable = True
        form.data['author'] = user
        if form.is_valid():
            form.save()
            messages.success(request, 'Your ticket has been saved!')
            return redirect('/new_ticket/')
        else:
            messages.warning(request, 'Please check the field entries.')
            return redirect('/new_ticket/')
    else:
        form = TicketForm(initial={'author':user})
        return render(request, "Btapp/new_ticket.html", {"form":form}) # HttpResponse object, render is just a shortcut

class TicketIndexView(generic.ListView): # Generic display views
    template_name = 'Btapp/ticket_index.html'
    context_object_name = 'ticket_list'
    def get_queryset(self): # Para los generic views los metodos ya estan definidos
        """Return the last five published questions."""
        return Ticket.objects.order_by('-opening_date') # Tiene que regresar un QuerySet object
        
class TicketDetailView(generic.DetailView):
    model = Ticket
    template_name = 'Btapp/ticket_detail.html'

"""def ticket_index(request):
    ticket_list = Ticket.objects.order_by('-opening_date')
    context = {'ticket_list': ticket_list}
    return render(request, 'Btapp/ticket_index.html', context)
def ticket_detail(request, id):
    ticket = get_object_or_404(Ticket, pk=id) # get_object_or_404 would couple the model layer to the view layer.
    return render(request, 'Btapp/ticket_detail.html', {'ticket': ticket})"""


### PROYECTOS
@login_required()
def new_project(request):
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        request.POST._mutable = True
        form.data['author'] = user
        if form.is_valid():
            form.save()
            messages.success(request, 'Your project has been saved')
            return render(request, "Btapp/new_project.html", {"form":form})
        else:
            messages.warning(request, 'Please check the field entries.')
            return render(request, "Btapp/new_project.html", {"form":form})
    else:
        form = ProjectForm(initial={'author':user})
        return render(request, "Btapp/new_project.html", {"form":form})

class ProjectIndexView(generic.ListView):
    template_name = 'Btapp/project_index.html'
    context_object_name = 'project_list'
    def get_queryset(self): 
        return Project.objects.all() 

def project_detail(request, id):
    ticket_list = Ticket.objects.filter(project=id).order_by('-opening_date')
    return render(request, 'Btapp/ticket_index.html', {'ticket_list': ticket_list})


### Sign
def sign(request):
    if request.method == 'POST':
        form = SignForm(request.POST)
        if form.is_valid():
            cf = form.cleaned_data
            try:
                 validate_password(cf['password'], User(username=cf['username']))
            except: 
                messages.warning(request, 'The password is not valid. Please choose another.')
                return render(request, "accounts/sign.html", {'form':SignForm()})
            if not User.objects.filter(username=cf['username']):
                # el correo debe ser unico para cada usuario no se puede aletrar, afecta al reset password
                if not User.objects.filter(email=cf['email']):
                    if cf['password'] == cf['confirm_password']:
                        user = User.objects.create_user(cf['username'], cf['email'], cf['password'])
                        #profile = Profile(user=user,email=cf['email'])
                        user.save()
                        #profile.save()
                        login(request, user)
                        send_mail( "Confirmation of registration - BugTracker",
                                   "This is a registration confirmation email to the BugTracker page - Usuer (%s)" % (cf['username']), # Esto tenria que ser un archivo o almenos darle formato
                                   settings.DEFAULT_FROM_EMAIL,
                                   [cf['email']], 
                                   fail_silently=False,)
                        return redirect('/profile/')
                    else:
                        messages.warning(request, 'The two password fields did not match.')
                        return render(request, "accounts/sign.html", {"form":form}) 
                else:
                    messages.warning(request, 'Email address is already registered.')
                    return render(request, "accounts/sign.html", {"form":form})
            else:
                messages.warning(request, 'Username is already registered.')
                return render(request, "accounts/sign.html", {"form":form})  
        else:
            messages.warning(request, 'Please check the field entries.')
            return render(request, "accounts/sign.html", {"form":form})
    else:
        form = SignForm()
        return render(request, "accounts/sign.html", {'form':form})
