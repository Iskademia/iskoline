from django import forms
from .models import *
from department.models import *
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['user', 'email']

class AnnouncementForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Announce Something...'}
        ))

    image = forms.ImageField(required=False)

    class Meta:
        model = AnnouncementPost
        fields = ['body', 'image']

class PostForm(forms.ModelForm):
    # body = forms.CharField(
    #     label='',
    #     widget=forms.Textarea(
    #         attrs={'rows': '3',
    #                'placeholder': 'Say Something...'}
    #     ))

    # image = forms.ImageField(required=False)

    class Meta:
        model = Post
        fields = ['body', 'image', 'faculty']

class CommentForm(forms.ModelForm):
    # comment = forms.CharField(
    #     label='',
    #     widget=forms.Textarea(
    #         attrs={'rows': '3',
    #                'placeholder': 'Say Something...'}
    #     ))

    class Meta:
        model = Comment
        fields = ['comment']

class AnnouncementCommentForm(forms.ModelForm):
    # comment = forms.CharField(
    #     label='',
    #     widget=forms.Textarea(
    #         attrs={'rows': '3',
    #                'placeholder': 'Say Something...'}
    #     ))

    class Meta:
        model = AnnouncementComment
        fields = ['comment']

class RegistrarPostForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Say Something...'}
        ))

    image = forms.ImageField(required=False)

    class Meta:
        model = RegistrarPost
        fields = ['body', 'image']

class RegistrarCommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Say Something...'}
        ))

    class Meta:
        model = RegistrarComment
        fields = ['comment']

class ChairpersonPostForm(forms.ModelForm):
    body = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Say Something...'}
        ))

    image = forms.ImageField(required=False)

    class Meta:
        model = ChairpersonPost
        fields = ['body', 'image']

class ChairpersonCommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Say Something...'}
        ))

    class Meta:
        model = ChairpersonComment
        fields = ['comment']