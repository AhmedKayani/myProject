from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Crud

# Form for the user sign up page
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Form for the user login page
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

# Form for the CRUD App Main Page
class CrudForm(forms.ModelForm):
    class Meta:
        model = Crud
        fields = ['name', 'networth']