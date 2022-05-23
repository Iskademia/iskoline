from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.Faculty, name='facultyindex'),
    path('login/', views.loginPage, name="faclogin"),
    path('logout/', views.logoutUser, name="faclogout"),
    path('announcement', views.Announcement, name='facannouncement'),
    path('announcement/<int:pk>/', AnnouncementPostDetailView.as_view(), name='facannouncement_post_detail'),
    path('announcement/edit/<int:pk>/', AnnouncementPostEditView.as_view(), name='facannouncement_post_edit'),
    path('announcement/delete/<int:pk>/', AnnouncementPostDeleteView.as_view(), name='facannouncement_post_delete'),
    path('announcement/<int:post_pk>/comment/delete/<int:pk>/', AnnouncementCommentDeleteView.as_view(), name='facannouncement_comment_delete'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='facpost_detail'),
    path('post/<int:post_pk>/comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='faccomment_delete'),
]