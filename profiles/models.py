from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from .models import Profile

User = get_user_model()


def user_id(instance, filename):
    """Callable for upload_to argument in picture attribute below"""
    return f"user_{instance.user.id}/{filename}"


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=user_id, default="blank/no_img.png")
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    website = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=100, blank=True)


# Signals
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
