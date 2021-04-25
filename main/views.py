from django.shortcuts import render ,redirect
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import datetime


# Create your views here.

#homepage
def homepage(request):
    return render(request, "index.html")