from django.contrib.auth import views as auth_views

from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.LandingPage, name='index'),
    path('home', views.PostFeed, name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/edit/<int:pk>/', PostEditView.as_view(), name='post_edit'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/<int:pk>/', ProfileEditView.as_view(), name='profile_edit'),
    path('registrar', RegistrarPostListView.as_view(), name='registrar'),
    path('registrar/<int:pk>/', RegistrarPostDetailView.as_view(), name='registrar_post_detail'),
    path('registrar/edit/<int:pk>/', RegistrarPostEditView.as_view(), name='registrar_post_edit'),
    path('registrar/delete/<int:pk>/', RegistrarPostDeleteView.as_view(), name='registrar_post_delete'),
    path('registrar/<int:post_pk>/comment/delete/<int:pk>/', RegistrarCommentDeleteView.as_view(), name='registrar_comment_delete'),
    path('chairperson', ChairpersonPostListView.as_view(), name='chairperson'),
    path('chairperson/<int:pk>/', ChairpersonPostDetailView.as_view(), name='chairperson_post_detail'),
    path('chairperson/edit/<int:pk>/', ChairpersonPostEditView.as_view(), name='chairperson_post_edit'),
    path('chairperson/delete/<int:pk>/', ChairpersonPostDeleteView.as_view(), name='chairperson_post_delete'),
    path('chairperson/<int:post_pk>/comment/delete/<int:pk>/', ChairpersonCommentDeleteView.as_view(), name='chairperson_comment_delete'),
    path('announcement', AnnouncementView.as_view(), name='announcement'),
    path('announcement/<int:pk>/', AnnouncementPostDetailView.as_view(), name='announcement_post_detail'),
    path('announcement/edit/<int:pk>/', AnnouncementPostEditView.as_view(), name='announcement_post_edit'),
    path('announcement/delete/<int:pk>/', AnnouncementPostDeleteView.as_view(), name='announcement_post_delete'),
    path('announcement/student/view', AnnouncementStudentView.as_view(), name='announcement_student_view'),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),
    # Forgot Password
    path(
        'reset_password/',
        auth_views.PasswordResetView.as_view(),
        name='reset_password',
    ),
    path(
        'reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path(
        'reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete',
    ),
]