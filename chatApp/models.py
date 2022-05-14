from django.db import models
from django.contrib.auth.models import User
import uuid


# Create your models here.


class Rooms(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    roomname = models.CharField(max_length=255)
    rooms = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    datecreated = models.DateTimeField(auto_now_add=True)
    rndid = models.CharField(
        max_length=100, default=uuid.uuid4, editable=False, null=True, blank=True
    )

    def __str__(self):
        return self.roomname

    class Meta:
        ordering = ("datecreated",)


class Message(models.Model):
    username = models.CharField(max_length=255)
    room = models.CharField(max_length=255)
    content = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date_added",)
