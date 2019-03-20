from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('screenshot', 'description','url','title','owner')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'votes','project']

class VotesForm(forms.ModelForm):
    class Meta:
        model = Votes
        exclude = ['user']