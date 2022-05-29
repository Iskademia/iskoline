from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .models import *
from department.models import *
from department.models import *
from .forms import *
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CreateUserForm
import re

from django.contrib.auth.decorators import login_required


email_regex = "^[a-zA-Z_-]+@iskolarngbayan\.pup\.edu\.ph$"

#Login
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('post_list')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'home/login.html', context)

#Register
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('post_list')
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            print("email", email)
            if re.match(email_regex, email):
                form.save()
                return redirect('login')
            else:
                messages.info(request, 'Email Should be PUP Webmail only')
    context = {'form':form}
    return render(request, 'home/register.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

#Announcement Views
@login_required(login_url='login')
def AnnouncementView(request):
    if not request.user.email:
        return redirect("cplogout")
    posts = AnnouncementPost.objects.all().order_by('-date')
    context = {'announcement': posts}
    return render(request, 'home/announcement.html', context)

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

            return render(request, 'home/announcement_post_detail.html', context)

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

            return render(request, 'home/announcement_post_detail.html', context)

class AnnouncementCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = AnnouncementComment
    template_name = 'home/announcement_comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('announcement_post_detail', kwargs={'pk': pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

#General Feed Views
@login_required(login_url="login")
def PostFeed(request):
    if not request.user.email:
        return redirect("cplogout")
    posts = Post.objects.filter(faculty__isnull=True).order_by('-date')
    faculty = FacultyProfile.objects.all()
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(commit=False).author = request.user
            form.save()
        return redirect("post_list")
    context = {
            'post_list': posts,
            'faculty': faculty,
            'form': form,
        }
    return render(request, "home/post_list.html", context)

class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
            post = Post.objects.get(pk=pk)
            form = CommentForm()
            comments = Comment.objects.filter(post=post).order_by('-date')

            context = {
                'post': post,
                'form': form,
                'comments': comments,
            }

            return render(request, 'home/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user.profile
            post = Post.objects.get(pk=pk)
            form = CommentForm(request.POST)

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

            return render(request, 'home/post_detail.html', context)

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['body', 'image']
    template_name = 'home/post_edit.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post_detail', kwargs={'pk': pk})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'home/post_delete.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'home/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post_detail', kwargs={'pk': pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


#Profile Views
class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        if not request.user.email:
            return redirect("cplogout")
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-date')

        context = {
            'user': user,
            'profile': profile,
            'posts': posts
        }

        return render(request, 'home/profile.html', context)

class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['full_name', 'student_id', 'bio', 'gender', 'birth_date', 'location', 'picture']
    template_name = 'home/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile', kwargs={'pk': pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user



#Registrar Views
class RegistrarPostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = RegistrarPost.objects.filter(author=request.user).order_by('-date')
        form = RegistrarPostForm()
        
        context = {
            'registrar': posts,
            'form': form,
        }

        return render(request, 'home/registrar.html', context)

    def post(self, request, *args, **kwargs):
        posts = RegistrarPost.objects.filter(author=request.user).order_by('-date')
        form = RegistrarPostForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

        context = {
            'registrar': posts,
            'form': form,
        }

        return render(request, 'home/registrar.html', context)

class RegistrarPostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = RegistrarPost.objects.get(pk=pk)
        form = RegistrarCommentForm()
        comments = RegistrarComment.objects.filter(post=post).order_by('-date')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        return render(request, 'home/registrar_post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = RegistrarPost.objects.get(pk=pk)
        form = RegistrarCommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
        
        comments = RegistrarComment.objects.filter(post=post).order_by('-date')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        return render(request, 'home/registrar_post_detail.html', context)

class RegistrarPostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RegistrarPost
    fields = ['body','image']
    template_name = 'home/registrar_post_edit.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('registrar_post_detail', kwargs={'pk': pk})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class RegistrarPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = RegistrarPost
    template_name = 'home/registrar_post_delete.html'
    success_url = reverse_lazy('registrar')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class RegistrarCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = RegistrarComment
    template_name = 'home/registrar_comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('registrar_post_detail', kwargs={'pk': pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author



#Chairperson Views
class ChairpersonPostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = ChairpersonPost.objects.filter(author=request.user).order_by('-date')
        form = ChairpersonPostForm()
        
        context = {
            'chairperson': posts,
            'form': form,
        }

        return render(request, 'home/chairperson.html', context)

    def post(self, request, *args, **kwargs):
        posts = ChairpersonPost.objects.filter(author=request.user).order_by('-date')
        form = ChairpersonPostForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

        context = {
            'chairperson': posts,
            'form': form,
        }

        return render(request, 'home/chairperson.html', context)

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
        return render(request, 'home/chairperson_post_detail.html', context)

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
        return render(request, 'home/chairperson_post_detail.html', context)

class ChairpersonPostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ChairpersonPost
    fields = ['body', 'image']
    template_name = 'home/chairperson_post_edit.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('chairperson_post_detail', kwargs={'pk': pk})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class ChairpersonPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ChairpersonPost
    template_name = 'home/chairperson_post_delete.html'
    success_url = reverse_lazy('chairperson')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class ChairpersonCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = ChairpersonComment
    template_name = 'home/chairperson_comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('chairperson_post_detail', kwargs={'pk': pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author


# Faculty Views
@login_required(login_url='login')
def FacultyPost(request):
    posts = Post.objects.filter(author=request.user ,faculty__isnull=False).order_by('-date')
    context = {'faculty': posts}
    return render(request, 'home/faculty.html', context)


class FacultyPostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        form = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-date')

        context = {
            'post': post,
            'form': form,
            'comments': comments,
        }
        return render(request, 'home/faculty_post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)
        form = CommentForm(request.POST)

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
        return render(request, 'home/faculty_post_detail.html', context)

class FacultyPostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['body','image']
    template_name = 'home/faculty_post_edit.html'
    
    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('faculty_post_detail', kwargs={'pk': pk})
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class FacultyPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'home/faculty_post_delete.html'
    success_url = reverse_lazy('faculty')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class FacultyCommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'home/faculty_comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('faculty_post_detail', kwargs={'pk': pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author



def LandingPage(request):
    if request.user.is_authenticated:
        if not request.user.email:
            return redirect("cplogout")
        else: 
            return redirect('post_list')
    context = {
    }
    return render(request, 'home/index.html', context)
