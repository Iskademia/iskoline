from django.urls import path
from . import views

urlpatterns = [
    # path('', views.Fronpage, name='chat'),
    path('', views.Index, name='chatindex'),
    path("chat/<str:room_name>/", views.Room, name='room'),
    path("room", views.EnterRoom, name='enterroom'),
    # Save Room
    path("savedroom", views.SaveRoom, name='saveroom'),
    path("updateroom/<str:pk>", views.UpdateRoom, name='update'),
    path("deleteroom/<str:pk>", views.DeleteRoom, name='delete'),
]