from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from pyuploadcare.dj.models import ImageField
from pyuploadcare.dj.forms import FileWidget
from django.conf import settings
from django.db.models import Avg, Max, Min
# import numpy as np

# Create your models here.


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Project(models.Model):
    screenshot = ImageField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    url = models.CharField(max_length=255)
    owner = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True, null=True)
    design=models.PositiveIntegerField(choices=list(zip(range(1,11), range(1,11))), default=1)
    usability = models.PositiveIntegerField(choices=list(zip(range(1, 11), range(1, 11))), default=1)
    content = models.PositiveIntegerField(choices=list(zip(range(1, 11), range(1, 11))), default=1)
    remarks = models.CharField(max_length=50,null=True)

    class Meta:
        ordering = ['-pk']

    def save_project(self):
        self.save()


    def delete_image(self):
        self.delete()

    def __str__(self):

        return self.title

    @classmethod
    def get_by_id(cls, id):
        details = Project.objects.filter(owner=id)
        return details

    @classmethod
    def get_all_projects(cls):
        project = Project.objects.all()
        return project

    @classmethod
    def search_by_project(cls, search_term):
        project = Project.objects.filter(title__icontains=search_term)
        return project


class Profile(models.Model):
    profile_pic = models.ImageField(upload_to = 'profile/',blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Bio = models.CharField(max_length = 255,null = True)
    email = models.EmailField(null = True)
    address = models.CharField(max_length=255, null = True)
    phone_number = models.IntegerField( null = True)
    full_name = models.CharField(max_length=255, null=True)
    project = models.ForeignKey(Project,null=True)

    def __str__(self):
        return self.user.username

    def save_profile(self):
        self.save()

    @classmethod
    def get_by_id(cls, id):
        details = Profile.objects.get(user=id)
        return details

    @classmethod
    def filter_by_id(cls, id):
        details = Profile.objects.filter(user=id).first()
        return details


