from django.test import TestCase
from .models import TicketForm, Project
from django.contrib.auth.models import User
from django.db import models

# Create your tests here.
class TestAForm(TestCase): # py manage.py test BugT.tests.ReportedeBugsTests
    """
    Test Ticket's form
    """
    def test_form(self):
        user = User()
        project = Project()
        form_data = {'author':user, 'project':project, 'description':'Lo que sea'}
        form_instance = TicketForm(data=form_data)
        self.assertTrue(form_instance.is_valid()) # hay que agregar a data stage y level no pueden estar vacios

class TestAFormP(TestCase): # py manage.py test BugT.tests.ReportedeBugsTests
    """
    Test Project's form
    """
    def test_form(self):
        user = User(username='Boris') 
        self.assertTrue(user.username, 'Boris')
        form_data = {'author':user, 'title':'Lo que sea'}
        form_instance = TicketForm(data=form_data)
        self.assertTrue(form_instance.data, form_data)
        print(form_instance.data)
        self.assertTrue(form_instance.is_valid()) # es falso

class TestOverrideUserModel(TestCase):
    """
    Test extending the existing User model INCOMPLETOOO
    """
    class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, help_text="Use the format ###-###-####", null=True, blank=True)
    profile_pic = models.ImageField(default='img/profile_pic/user.jpg', blank=True, null=True, upload_to = 'img/profile_pic') 

    class ProfileForm(ModelForm):
        class Meta:
            model = Profile
            fields = '__all__'
            exclude = ['user']
            labels = {'profile_pic': _('Profile Picture')}