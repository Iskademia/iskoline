from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

from student.models import *

# class ChairpersonsComment(models.Model):
#     comment = models.TextField()
#     date = models.DateTimeField(default=timezone.now)
#     post = models.ForeignKey(ChairpersonPost, on_delete=models.CASCADE)
#     author = models.ForeignKey(User, on_delete=models.CASCADE)


class FacultyProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, verbose_name='user', related_name='facultyprofile', on_delete=models.CASCADE)
    name = models.CharField(max_length=30, blank=True, null=True)
    is_faculty = models.BooleanField(default=True, verbose_name='is_faculty')
    is_chairperson = models.BooleanField(default=False, verbose_name='is_chairperson')

class AnnouncementPost(models.Model):
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)

class AnnouncementComment(models.Model):
    comment = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('AnnouncementPost', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

