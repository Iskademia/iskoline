from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# from sqlalchemy import false

class Post(models.Model):
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)
    faculty = models.CharField(max_length=30, blank=True, null=True)

class Comment(models.Model):
    comment = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=200, null=True)
    bio = models.TextField(max_length=50, blank=True, null=True)
    birth_date=models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='uploads/profile_pictures', blank=True)
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    gender = models.CharField(max_length=6, blank=True, null=True ,choices=GENDER_CHOICES)
    student_id = models.CharField(max_length=16, blank=False, null=True)

class RegistrarPost(models.Model):
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)

class RegistrarComment(models.Model):
    comment = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('RegistrarPost', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class ChairpersonPost(models.Model):
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)

class ChairpersonComment(models.Model):
    comment = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('ChairpersonPost', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()