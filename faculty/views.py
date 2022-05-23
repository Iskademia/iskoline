from calendar import c
from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView, DeleteView


from .forms import *
from department.models import *
from .models import *
from student.models import *


# Create your views here.
@login_required(login_url='faclogin')
def Faculty(request):
    if request.user.email:
        return redirect("post_list")
    posts = Post.objects.filter(faculty=request.user).order_by('-date')
    context = {
            'post_list': posts,
        }
    return render(request, 'faculty/faculty_post.html', context)


@login_required(login_url="faclogin")
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
        return redirect("facannouncement")
    context = {
            'announcement': posts,
            'form': form,
        }
    return render(request, "faculty/announcement.html", context)

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

            return render(request, 'faculty/announcement_post_detail.html', context)

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

            return render(request, 'faculty/announcement_post_detail.html', context)

class AnnouncementPostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = AnnouncementPost
    fields = ['body','image']
    template_name = 'department/announcement_post_edit.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('facannouncement_post_detail', kwargs={'pk': pk})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class AnnouncementPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AnnouncementPost
    template_name = 'faculty/announcement_post_delete.html'
    success_url = reverse_lazy('facannouncement')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class AnnouncementCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AnnouncementComment
    template_name = 'faculty/announcement_comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('facannouncement_post_detail', kwargs={'pk': pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
            post = Post.objects.get(pk=pk)
            form = FacultyComment()
            comments = Comment.objects.filter(post=post).order_by('-date')

            context = {
                'post': post,
                'form': form,
                'comments': comments,
            }

            return render(request, 'faculty/faculty_post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user.profile
            post = Post.objects.get(pk=pk)
            form = FacultyComment(request.POST)

            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.author = request.user
                new_comment.post = post
                new_comment.save()
            
            comments = Comment.objects.filter(post=post).order_by('-date')

            context = {
                'post': post,
                'form': form,
                'comments': comments,
            }

            return render(request, 'faculty/faculty_post_detail.html', context)

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'faculty/faculty_post_comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('facpost_detail', kwargs={'pk': pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('facultyindex')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            faculty = FacultyProfile.objects.filter(user=user.id).values_list('is_faculty', flat=True)
            if faculty:           
                login(request, user)
                return redirect('facultyindex')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'faculty/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('faclogin')