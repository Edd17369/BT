from django.shortcuts import render, redirect, HttpResponse, get_object_or_404

from .models import Ticket, TicketForm, Project, ProjectForm
from django.contrib.auth.models import User

from django.contrib.auth import  login, logout, authenticate

from django.contrib import messages

from django.views import generic




# Create your views here.

### HOME
def home(request):
    return render(request, "Btapp/home.html")


### TICKETS

#@login_required # The view code is free to assume the user is logged in
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





