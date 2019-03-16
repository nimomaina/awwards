from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from pyuploadcare.dj.models import ImageField
from pyuploadcare.dj.forms import FileWidget

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()




class Project(models.Model):
    screenshot = ImageField()
    url = models.CharField(max_length=50)
    description = models.TextField()
    title = models.CharField(max_length=100)
    # profile = models.OneToOneField(Profile)

    def save_project(self):
        self.save()

    def __str__(self):
        return str(self.name)

    def save_image(self):
        self.save()

    def delete_image(self):
        self.delete()

