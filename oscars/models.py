from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from pyuploadcare.dj.models import ImageField
from pyuploadcare.dj.forms import FileWidget

# Create your models here.


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()



class Profile(models.Model):
    profile_pic = models.ImageField(upload_to = 'profile/',blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    Bio = models.TextField(max_length = 255,null = True)
    votes = models.ManyToManyField('Project', related_name='pic', max_length=30)


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
    profile = models.ForeignKey(Profile, null=True, related_name='project')
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    # profile = models.OneToOneField(Profile)
    class Meta:
        ordering = ['-pk']

    def save_project(self):
        self.save()

    def __str__(self):
        return str(self.name)

    def delete_image(self):
        self.delete()

    @classmethod
    def get_project(cls, profile):
        project = Project.objects.filter(Profile__pk=profile)
        return project

    @classmethod
    def get_all_projects(cls):
        project = Project.objects.all()
        return project

    @classmethod
    def search_by_profile(cls, search_term):
        projo = cls.objects.filter(profile__name__icontains=search_term)
        return projo

    @classmethod
    def get_profile_projects(cls, profile):
        project = Project.objects.filter(profile__pk=profile)
        return project

    @classmethod
    def find_project_id(cls, id):
        identity = Project.objects.get(pk=id)
        return identity


class Votes(models.Model):
    design = models.CharField(max_length=100)
    usability = models.CharField(max_length=100)
    content = models.CharField(max_length=100, blank=True, null=True)
    average = models.FloatField(max_length=50)
    user = models.ForeignKey(User, null=True)
    project = models.ForeignKey(Project, related_name='rate', null=True)

    def __str__(self):
        return self.design

    class Meta:
        ordering = ['-id']

    def save_rate(self):
        self.save()

    @classmethod
    def get_votes(cls, profile):
        votes = Votes.objects.filter(Profile__pk=profile)
        return votes

    @classmethod
    def get_all_votes(cls):
        all_votes = Votes.objects.all()
        return all_votes
