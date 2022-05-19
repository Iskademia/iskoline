from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.utils.datastructures import MultiValueDictKeyError


import uuid

from .forms import *

from .models import *


# # Create your views here.

# def Chat(request):
#     # if request.user.is_authenticated:
#     #     return redirect('index')
#     return render(request, 'chatApp/index.html')


# @login_required(login_url='login')
def Index(request):
    randROOM = None
    rooms = Rooms.objects.filter(user=request.user)
    if request.method == "POST":
        randROOM = str(uuid.uuid4().hex)
    context = {'randROOM': randROOM, 'rooms': rooms}
    return render(request, 'chatApp/dashboard.html', context)


@login_required(login_url='login')
def EnterRoom(request):
    rooms = Rooms.objects.filter(user=request.user)
    if request.method == "POST":
        roomName = request.POST['roomName']
        return redirect('chat/{}'.format(roomName))

    return render(request, 'chatApp/gotoroom.html', {'rooms': rooms})


@login_required(login_url='login')
def SaveRoom(request):
    roomform = RoomsForm()
    rooms = Rooms.objects.filter(user=request.user)
    if request.method == 'POST':
        roomform = RoomsForm(request.POST)
        if roomform.is_valid():
            roomform.save(commit=False).user = request.user
            roomform.save()
        return redirect("chatindex")
    context = {'form': roomform, 'rooms': rooms}
    return render(request, 'chatApp/savedroom.html', context)


@login_required(login_url='login')
def Room(request, room_name):
    rooms = Rooms.objects.filter(user=request.user)

    username = request.user
    messages = Message.objects.filter(room=room_name)[0:]
    return render(
        request,
        'chatApp/room.html',
        {
            'room_name': room_name,
            'username': username,
            'messages': messages,
            'rooms': rooms,
        },
    )

@login_required(login_url='login')
def UpdateRoom(request, pk):
    room = Rooms.objects.get(rndid=pk)
    roomform = RoomsForm(instance=room)

    if request.method == 'POST':
        roomform = RoomsForm(request.POST, instance=room)
        if roomform.is_valid():
            roomform.save(commit=False).user = request.user
            roomform.save()
        return redirect('chatindex')
    return render(request, 'chatApp/update.html', {'rooms': roomform, 'randid': pk})


@login_required(login_url='login')
def DeleteRoom(request, pk):
    room = Rooms.objects.get(rndid=pk)
    messages = Message.objects.filter(room=room.rooms)

    if request.method == 'POST':
        room.delete()
        messages.delete()
        return redirect('chatindex')

    return render(request, 'chatApp/delete.html', {'room': room, 'randid': pk})
