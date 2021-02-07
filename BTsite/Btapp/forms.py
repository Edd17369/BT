from django import forms
from django.contrib.auth.password_validation import password_validators_help_text_html

class SignForm(forms.Form):
    username = forms.CharField(max_length=50, help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.")
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, help_text=password_validators_help_text_html)
    confirm_password = forms.CharField(widget=forms.PasswordInput, help_text="Enter the same password as before, for verification.")


