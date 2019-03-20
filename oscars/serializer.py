from rest_framework import serializers
from .models import *

class Project(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('__all__')

class Profile(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('__all__')