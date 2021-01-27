from django.shortcuts import render, redirect, HttpResponse

from .models import Ticket, TicketForm, Project, ProjectForm
from django.contrib.auth.models import User

from django.contrib.auth import  login, logout, authenticate

from django.contrib import messages
# Create your views here.


#def home(request):
#    return render(request, "home.html")

#@login_required # The view code is free to assume the user is logged in
def new_ticket(request):
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your ticket has been saved!')
            return redirect('/new_ticket/')
        else:
            messages.warning(request, 'Please check the field entries.')
            return redirect('/new_ticket/')
        pass
    else:
        form = TicketForm(initial={'author':user})
        return render(request, "Btapp/new_ticket_form.html", {"form":form}) # HttpResponse object, render is just a shortcut

def new_project(request):
    user = User.objects.get(username=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your project has been saved')
            return render(request, "Btapp/new_project_form.html", {"form":form})
        else:
            messages.warning(request, 'Please check the field entries.')
            render(request, "Btapp/new_project_form.html", {"form":form})
    else:
        form = ProjectForm(initial={'author':user})
        return render(request, "Btapp/new_project_form.html", {"form":form})