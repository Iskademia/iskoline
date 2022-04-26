from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from .models import *
from .forms import *
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-date')
        form = PostForm()
        
        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'home/post_list.html', context)

    def post(self, request, *args, **kwargs):
        posts = Post.objects.all().order_by('-date')
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()

        context = {
            'post_list': posts,
            'form': form,
        }

        return render(request, 'home/post_list.html', context)

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
    fields = ['body']
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


class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
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
    fields = ['name', 'bio', 'birth_date', 'location', 'picture']
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
        posts = RegistrarPost.objects.all().order_by('-date')
        form = RegistrarPostForm()
        
        context = {
            'registrar': posts,
            'form': form,
        }

        return render(request, 'home/registrar.html', context)

    def post(self, request, *args, **kwargs):
        posts = RegistrarPost.objects.all().order_by('-date')
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
    fields = ['body']
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