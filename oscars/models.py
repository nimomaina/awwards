from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    screenshot = models.ImageField(default='default.jpg', blank=True, manual_crop='')
    url = models.CharField(max_length=50)
    description = models.TextField()
    profile = models.OneToOneField(Profile)
