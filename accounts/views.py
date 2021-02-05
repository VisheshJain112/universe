from django.core.checks import messages
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import AD_User
import pandas as pd
# Create your views here.
from django.db.models import Q
import numpy as np
import json
from django.template.defaultfilters import register
from pathlib import Path
import os
# Create your views here.
def login(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['pass']



        if AD_User.objects.filter(username=username,password=password).exists():


            
            messages.info(request,'Granted')
            
            request.session['username'] = username # set 'token' in the session
            request.session['password'] = password


      
            return redirect("terms")
        else:
            messages.info(request, 'Invalid Credentials')
            return redirect('login')


    else:
        return render(request,'login.html')