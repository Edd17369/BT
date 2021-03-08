from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

# Models
from .models import Ticket, TicketForm, Project, ProjectForm, Profile, ProfileForm, Membership, Comment, CommentForm
from django.contrib.auth.models import User

# Forms
from .forms import SignForm, Contact

# Authentication
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.password_validation import validate_password, password_validators_help_text_html
from django.conf import settings
from django.core.mail import send_mail

# Messages
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

# Generic Views
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin 

# Graphs
from collections import defaultdict
from plotly.offline import plot
import plotly.graph_objs as go
#import pandas as pd #Sunplot
import plotly.express as px #Sunplot



### HOME
def home(request):
    return render(request, "Btapp/home.html")


### TICKETS
class AddTicket(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'Btapp/new_ticket.html'
    success_url = '/new_ticket/'
    success_message = "Ticket was created successfully"
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class TicketIndexView(generic.ListView): # Generic display views, automaticamente recibe el object.pk de la url
    template_name = 'Btapp/ticket_index.html'
    context_object_name = 'ticket_list'
    def get_queryset(self): # Sobrescribir el metodo
        return Ticket.objects.order_by('-opening_date') # Tiene que regresar un QuerySet object
        
class TicketDetailView(generic.DetailView):
    model = Ticket
    template_name = 'Btapp/ticket_detail.html'

@login_required
def delete_ticket(request, pk): # No tiene mucho sentido eliminar un ticket
    user = User.objects.get(username=request.user)
    ticket = Ticket.objects.get(pk=pk)
    if request.method == 'POST':
        if request.user == ticket.author:
            ticket.delete()
            ticket_list = Ticket.objects.order_by('-opening_date')
            return render(request, "Btapp/ticket_index.html", {'ticket_list':ticket_list})
        else:
            messages.warning(request, "Only the ticket's author can delet it.")
            return render(request, "Btapp/ticket_detail.html", {'ticket':ticket})
    else:
        return render(request, "Btapp/ticket_confirm_delete.html", {'object':ticket})
    
@login_required
def update_ticket(request, pk):
    user = User.objects.get(username=request.user)
    ticket = Ticket.objects.get(pk=pk)
    form = TicketForm(instance=ticket)
    if request.method == 'POST':
        if request.user == ticket.author:
            form = TicketForm(request.POST, request.FILES, instance=ticket)
            request.POST._mutable = True 
            form.data['author'] = user
            if form.is_valid():
                messages.success(request, 'Your ticket has been updated!')
                form.save()
                return render(request, "Btapp/ticket_update.html", {'form':form})
            else:
                messages.warning(request, 'Please check the field entries.')
                return render(request, "Btapp/ticket_update.html", {'form':form})
        else:
            messages.warning(request, "Only the ticket's author can edit it.")
            return render(request, "Btapp/ticket_update.html", {'form':form})
    else:
        return render(request, "Btapp/ticket_update.html", {'form':form})


### COMMENTS
class AddComment(LoginRequiredMixin, generic.CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'Btapp/new_comment.html'
    #success_message = "Your comment [%(name)s] was created successfully"
    def form_valid(self, form):
        form.instance.ticket_id = self.kwargs['pk']
        form.instance.author = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('ticket_detail', kwargs={'pk': self.kwargs['pk']})
        # We have to use reverse_lazy() instead of reverse(), as the urls are not loaded when the file is imported.

    

### PROYECTOS
class AddProject(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'Btapp/new_project.html'
    #initial = {'members':self.request.user}
    success_url = '/new_project/'
    success_message = "Project [%(name)s] was created successfully"
    # save() creates and saves a database object from ALL the data bound to the form, incluido el modelo "Membership"

class ProjectIndexView(generic.ListView):
    template_name = 'Btapp/project_index.html'
    context_object_name = 'project_list'
    def get_queryset(self): 
        return Project.objects.order_by('-registration_date')

class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = 'Btapp/project_detail.html'

@login_required
def update_project(request, pk):
    user = User.objects.get(username=request.user)
    project = Project.objects.get(pk=pk)
    form = ProjectForm(instance=project)
    if request.method == 'POST':
        if project.has_user(user):
            form = ProjectForm(request.POST, instance=project)
            if form.is_valid():
                messages.success(request, 'Your project has been updated!')
                form.save()
                return render(request, "Btapp/project_update.html", {'form':form})
            else:
                messages.warning(request, 'Please check the field entries.')
                return render(request, "Btapp/project_update.html", {'form':form})
        else:
            messages.warning(request, "Only project members can edit it.")
            return render(request, "Btapp/project_update.html", {'form':form})
    else:
        return render(request, "Btapp/project_update.html", {'form':form})
    


### USERS
class  UsersIndexView(generic.ListView):
    template_name = 'Btapp/user_index.html'
    context_object_name = 'user_list'
    def get_queryset(self):
        return User.objects.order_by('-username')


### ACCOUNTS
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
            # El correo y el username deben ser unicos para cada usuario y no se pueden alterar
            if not User.objects.filter(username=cf['username']):
                if not User.objects.filter(email=cf['email']):
                    if cf['password'] == cf['confirm_password']:
                        user = User.objects.create_user(cf['username'], cf['email'], cf['password'])
                        profile = Profile(user=user, email=cf['email'])
                        user.save()
                        profile.save()
                        login(request, user)
                        send_mail( "Confirmation of registration - BugTracker",
                                   "This is a registration confirmation email to the BugTracker page - Usuer (%s)" % (cf['username']), # Esto tenria que ser un archivo o almenos darle formato
                                   settings.DEFAULT_FROM_EMAIL,
                                   [cf['email']], 
                                   fail_silently=False,)
                        return redirect('/accounts/profile/')
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


### Profile
def profile(request):
    user = User.objects.get(username=request.user) # un caso si user es anonimo entonces que lo redirija a login
    #projects = [p for p in Project.objects.filter(author=user) if p.has_open_tickets()]
    projects = [p for p in Project.objects.all() if p.has_open_tickets() and p.has_user(user)]
    # Grafica de barras
    projectsT = [p.name for p in projects]
    r = [len(Ticket.objects.filter(project=pj, author=user, stage=20)) for pj in projects]
    w = [len(Ticket.objects.filter(project=pj, author=user, stage=60)) for pj in projects]
    c = [len(Ticket.objects.filter(project=pj, author=user, stage=80)) for pj in projects]
    fig = go.Figure(
        data=[
            go.Bar(name='Registered', x=projectsT, y=r, marker_color = ['rgb(8, 94, 255)',]*len(projectsT)),
            go.Bar(name='Working on', x=projectsT, y=w, marker_color = ['rgb(255, 251, 14)',]*len(projectsT)),
            go.Bar(name='Closed', x=projectsT, y=c, marker_color = ['rgb(243, 12, 58)',]*len(projectsT))
            ])
    fig.update_layout(
            title='Your tickets per project.',
            xaxis_tickfont_size=14,
            yaxis=dict(title='Amount of tickets by stage', titlefont_size=16, tickfont_size=14),
            legend=dict(bgcolor='rgba(255, 255, 255, 0)', bordercolor='rgba(255, 255, 255, 0)'),
            barmode='group',
            bargap=0.15, # gap between bars of adjacent location coordinates.
            bargroupgap=0 # gap between bars of the same location coordinate.
            )
    graphBar = plot(fig, auto_open = False, output_type="div")
    if  request.method == 'POST':
        select = request.POST.get("project")
        if select:
            # Grafica pastel
            p = Project.objects.get(id=select)
            tickets = list(Ticket.objects.filter(project=p, author=user))
            sizes = {'Closed':defaultdict(lambda:1), 'Working on':defaultdict(lambda:1), 'Registered':defaultdict(lambda:1)}
            for t in tickets:
                sizes[t.get_stage_display()][t.get_level_display()] += 1
            a = [v for k, v in sizes['Closed'].items()]
            trace1 = go.Pie(labels=list(sizes['Closed'].keys()), values=[v*100/sum(a) for v in a], hole=0.6, 
                        domain=dict(x=[0, 0.2]), marker=dict(line=dict(color=' #343434', width=2)), )
            b = [v for k, v in sizes['Working on'].items()]
            trace2 = go.Pie(labels=list(sizes['Working on'].keys()), values=[v*100/sum(b) for v in b], hole=0.6, 
                        domain=dict(x=[0.3, 0.5]), marker=dict(line=dict(color=' #343434', width=2)), )
            c = [v for k, v in sizes['Registered'].items()]
            trace3 = go.Pie(labels=list(sizes['Registered'].keys()), values=[v*100/sum(c) for v in c], hole=0.6, 
                        domain=dict(x=[0.6, 0.8]), marker=dict(line=dict(color=' #343434', width=2)), )     
            #layout = go.Layout(title="%s's tickets" % (p.name),)
            data = [trace1, trace2, trace3]
            fig2 = go.Figure(data=data, ) #layout=layout
            fig2.update_layout(
                annotations=[dict(text='Closed', x=0.07, y=0.5, font_size=15, showarrow=False),
                            dict(text='Working on', x=0.4, y=0.5, font_size=15, showarrow=False),
                            dict(text='Registered', x=0.75, y=0.5, font_size=15, showarrow=False)]) # Add annotations in the center of the donut pies.
            graphPie = plot(fig2, auto_open = False, output_type="div")
            context = {'user':user, 'reports':tickets, 'projects':projects, 'pieplot':graphPie, 'barplot':graphBar, 'project':p.name}
            return render(request, "Btapp/dashboard.html", context)
        else:
            messages.warning(request, 'Please select an option.')
            context = {'user':user, 'projects':projects, 'barplot':graphBar}
            return render(request, "Btapp/dashboard.html", context)
    else:
        context = {'user':user, 'projects':projects, 'barplot':graphBar}
        return render(request, "Btapp/dashboard.html", context)


@login_required
def setting_profile(request):
    user = User.objects.get(username=request.user)
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return render(request, "accounts/settings_profile.html", {"form":form, "user":user})
        else:
            messages.error(request, 'Your profile could not be updated.')
            return render(request, "accounts/settings_profile.html", {"form":form, "user":user})
    else:
        form = ProfileForm(instance=profile)
        return render(request, "accounts/settings_profile.html", {"form":form, "user":user})


def profile_img(request):
    user = request.user
    return render(request, "base.html", {'user':user})


### CONTACT
def contact(request):
    if request.method == 'POST':
        form = Contact(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            send_mail(
                data['subject']+'-'+'Username: '+data['username'],
                data['message']+'\n'+'From: '+data['email'],
                settings.DEFAULT_FROM_EMAIL, # De donde se envia el correo
                ['falsodonfalso@gmail.com'], # A donde envia el correo, no envia al correo que diste en DEFAULT_FROM_EMAIL 
                fail_silently=False,)
            messages.success(request, 'Your email has been sent. Thank you for contacting us')
            return render(request, "Btapp/contact.html", {'form':form})
        else:
            messages.error(request, 'Your email has not been sent.')
            return render(request, "Btapp/contact.html", {'form':form})
    else:
        form = Contact()
        return render(request, "Btapp/contact.html", {'form':form})