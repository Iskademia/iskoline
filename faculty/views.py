from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.utils.datastructures import MultiValueDictKeyError


import uuid

# from .forms import *

from .models import *


# Create your views here.

def Faculty(request):
    # if request.user.is_authenticated:
    #     return redirect('index')
    return render(request, 'faculty/index.html')