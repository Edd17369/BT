from django.test import TestCase
from .models import TicketForm, Project
from django.contrib.auth.models import User

# Create your tests here.
class TestAForm(TestCase): # py manage.py test BugT.tests.ReportedeBugsTests
    def test_form(self):
        user = User()
        project = Project()
        form_data = {'author':user, 'project':project, 'description':'Lo que sea'}
        form_instance = TicketForm(data=form_data)
        self.assertTrue(form_instance.is_valid()) # hay que agregar a data stage y level no pueden estar vacios

class TestAFormP(TestCase): # py manage.py test BugT.tests.ReportedeBugsTests
    def test_form(self):
        user = User(username='Boris') 
        self.assertTrue(user.username, 'Boris')
        form_data = {'author':user, 'title':'Lo que sea'}
        form_instance = TicketForm(data=form_data)
        self.assertTrue(form_instance.data, form_data)
        print(form_instance.data)
        self.assertTrue(form_instance.is_valid()) # es falsoo