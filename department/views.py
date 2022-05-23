from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils.datastructures import MultiValueDictKeyError
from django.views import View
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView

import uuid

from .forms import *

from .models import *
from student.models import *

# Create your views here.

@login_required(login_url='cplogin')
def Chairperson(request):
    if request.user.email:
        return redirect("post_list")
    posts = ChairpersonPost.objects.all().order_by('-date')
    context = {'chairperson': posts}
    return render(request, 'department/chairpersonpost.html', context)

@login_required(login_url="cplogin")
def Announcement(request):
    if request.user.email:
        return redirect("post_list")
    posts = AnnouncementPost.objects.all().order_by('-date')
    form = AnnouncementForm()
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False).author = request.user
            form.save()
        return redirect("cpannouncement")
    context = {
            'announcement': posts,
            'form': form,
        }
    return render(request, "department/announcement.html", context)

class ChairpersonPostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = ChairpersonPost.objects.get(pk=pk)
        form = ChairpersonCommentForm()
        comments = ChairpersonComment.objects.filter(post=post).order_by('-date')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        return render(request, 'department/chairpersoncomment.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = ChairpersonPost.objects.get(pk=pk)
        form = ChairpersonCommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
        
        comments = ChairpersonComment.objects.filter(post=post).order_by('-date')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        return render(request, 'department/chairpersoncomment.html', context)


class AnnouncementPostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
            post = AnnouncementPost.objects.get(pk=pk)
            form = AnnouncementCommentForm()
            comments = AnnouncementComment.objects.filter(post=post).order_by('-date')

            context = {
                'post': post,
                'form': form,
                'comments': comments,
            }

            return render(request, 'department/announcement_post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user.profile
            post = AnnouncementPost.objects.get(pk=pk)
            form = AnnouncementCommentForm(request.POST)

            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.author = request.user
                new_comment.post = post
                new_comment.save()
            
            comments = AnnouncementComment.objects.filter(post=post).order_by('-date')

            context = {
                'post': post,
                'form': form,
                'comments': comments,
            }

            return render(request, 'department/announcement_post_detail.html', context)

class AnnouncementPostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AnnouncementPost
    fields = ['body','image']
    template_name = 'department/announcement_post_edit.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('cpannouncement_post_detail', kwargs={'pk': pk})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class AnnouncementPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AnnouncementPost
    template_name = 'department/announcement_post_delete.html'
    success_url = reverse_lazy('cpannouncement')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class AnnouncementCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AnnouncementComment
    template_name = 'department/announcement_comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('cpannouncement_post_detail', kwargs={'pk': pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('chairpersonindex')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            faculty = FacultyProfile.objects.filter(user=user.id).values_list('is_faculty', flat=True)
            if faculty:           
                login(request, user)
                return redirect('chairpersonindex')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'department/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('cplogin')