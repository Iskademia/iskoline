from django.urls import path
from . import views

urlpatterns = [
    # path('', views.Fronpage, name='chat'),
    path('', views.Department, name='departmentindex'),
]