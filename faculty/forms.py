from django import forms
from .models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from department.models import *
from student.models import *

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = AnnouncementPost
        fields = ['body', 'image']

class AnnouncementCommentForm(forms.ModelForm):
    class Meta:
        model = AnnouncementComment
        fields = ['comment']

class FacultyComment(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']