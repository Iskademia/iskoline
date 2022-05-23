from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('chairperson/', views.Chairperson, name='chairpersonindex'),
    path('comment/<int:pk>/', ChairpersonPostDetailView.as_view(), name='comment'),
    path('login/', views.loginPage, name="cplogin"),
    path('logout/', views.logoutUser, name="cplogout"),
    path('announcement', views.Announcement, name='cpannouncement'),
    path('announcement/<int:pk>/', AnnouncementPostDetailView.as_view(), name='cpannouncement_post_detail'),
    path('announcement/edit/<int:pk>/', AnnouncementPostEditView.as_view(), name='cpannouncement_post_edit'),
    path('announcement/delete/<int:pk>/', AnnouncementPostDeleteView.as_view(), name='cpannouncement_post_delete'),
    path('announcement/<int:post_pk>/comment/delete/<int:pk>/', AnnouncementCommentDeleteView.as_view(), name='cpannouncement_comment_delete'),
]