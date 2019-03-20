from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from pyuploadcare.dj.models import ImageField
from pyuploadcare.dj.forms import FileWidget
from django.conf import settings
from django.db.models import Avg, Max, Min
import numpy as np

# Create your models here.


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Profile(models.Model):
    profile_pic = models.ImageField(upload_to = 'profile/',blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Bio = models.CharField(max_length = 255,null = True)
    email = models.EmailField(null = True)
    address = models.CharField(max_length=255, null = True)
    phone_number = models.IntegerField( null = True)
    full_name = models.CharField(max_length=255, null=True)


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

    @classmethod
    def search_user(cls, name):
        userprof = Profile.objects.filter(user__username__icontains=name)
        return userprof

class Project(models.Model):
    screenshot = ImageField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    url = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    profile = models.ForeignKey(Profile, null=True,related_name='project')
    owner = models.ForeignKey(User,null = True, on_delete=models.CASCADE,)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-pk']

    def save_project(self):
        self.save()


    def delete_image(self):
        self.delete()

    def __str__(self):
        return self.owner

    @classmethod
    def get_project(cls, profile):
        project = Project.objects.filter(Profile__pk=profile)
        return project

    @classmethod
    def get_all_projects(cls):
        project = Project.objects.all()
        return project

    @classmethod
    def search_by_project(cls, search_term):
        project = Project.objects.filter(title__icontains=search_term)
        return project

    @classmethod
    def get_profile_projects(cls, profile):
        project = Project.objects.filter(profile__pk=profile)
        return project

    def average_design(self):
        design_ratings = list(map(lambda x: x.design_rating, self.reviews.all()))
        return np.mean(design_ratings)

    def average_usability(self):
        usability_ratings = list(map(lambda x: x.usability_rating, self.reviews.all()))
        return np.mean(usability_ratings)

    def average_content(self):
        content_ratings = list(map(lambda x: x.content_rating, self.reviews.all()))
        return np.mean(content_ratings)

class Votes(models.Model):

    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),

    )
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='votes')
    comment = models.TextField()
    design_rating = models.IntegerField(choices=RATING_CHOICES, default=0)
    usability_rating = models.IntegerField(choices=RATING_CHOICES, default=0)
    content_rating = models.IntegerField(choices=RATING_CHOICES, default=0)
    created_date = models.DateTimeField(auto_now_add=True, null=True)

    def save_review(self):
        self.save()

    def delete_comment(self):
        Votes.objects.get(id=self.id).delete()

    @classmethod
    def get_comment(cls, id):
        comments = Votes.objects.filter(project__pk=id)
        return comments

    def delete_review(self):
        self.delete()

    def __str__(self):
        return self.project

