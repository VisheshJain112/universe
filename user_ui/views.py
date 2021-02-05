from django.shortcuts import redirect, render
from accounts.models import AD_User,AD_Admin
import pandas as pd
from django.core.checks import messages
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse

from django.contrib import messages
from .models import user_input
import pandas as pd
# Create your views here.
from django.db.models import Q
import numpy as np
import json
from django.template.defaultfilters import register
from pathlib import Path
import os
# Create your views here.

def get_dropdown_values(pred_1_fp,pred_2_fp,pred_3_fp,recom_1_fp,recom_2_fp,recom_3_fp):
    f_1 = open(pred_1_fp)
    pred_1 = f_1.readlines()
    f_2 = open(pred_2_fp)
    pred_2 = f_2.readlines()
    f_3 = open(pred_3_fp)
    pred_3 = f_3.readlines()
    f_4 = open(recom_1_fp)
    recom_1 = f_4.readlines()
    f_5 = open(recom_2_fp)
    recom_2 = f_5.readlines()
    f_6 = open(recom_3_fp)
    recom_3 = f_6.readlines()
    return pred_1,pred_2,pred_3,recom_1,recom_2,recom_3

        

def user_ui(request):
    
    if request.method == "POST":
        print(request.POST)
        
        if request.POST.get("submit") is not None:
                
            pred_1 = request.POST['pred_1']
            pred_2 = request.POST['pred_2']
            pred_3 = request.POST['pred_3']
            recom_1 = request.POST['recom_1']
            recom_2 = request.POST['recom_2']
            recom_3 = request.POST['recom_3']
            username = request.session['username'] 
            password = request.session['password'] 
            casenum = request.session['casenum']


            user_inputs = user_input.objects.create(username = username,password = password,case_number = casenum,prediction_1=pred_1,prediction_2=pred_2,prediction_3=pred_3,recommendation_1 = recom_1,recommendation_2 = recom_2,recommendation_3 = recom_3)
            user_inputs.save();
            print("Created")
    
            return redirect('userinput')
        elif request.POST.get("home") is not None:
            return redirect('/index/index_case')
        elif request.POST.get("close") is not None:
            return redirect('/')
        elif request.POST.get("menu") is not None:
            return redirect('/accounts/login')
        else:
            return render(request,'error.html')

    else:
        username = "admin"
        password = "admin"

        all_users = AD_Admin.objects.all()
        for user in all_users:
            if user.username == username and user.password == password:

                prediction_1_dropdown = str(user.prediction_1_dropdown) 
                prediction_2_dropdown = str(user.prediction_2_dropdown) 
                prediction_3_dropdown = str(user.prediction_3_dropdown) 
                recommendation_1_dropdown = str(user.recommendation_1_dropdown) 
                recommendation_2_dropdown = str(user.recommendation_2_dropdown) 
                recommendation_3_dropdown = str(user.recommendation_3_dropdown) 
                
  
                BASE_DIR = Path(__file__).resolve().parent.parent
                recommendation_1_dropdown = os.path.join(BASE_DIR,"media",recommendation_1_dropdown)
                recommendation_2_dropdown = os.path.join(BASE_DIR,"media",recommendation_2_dropdown)
                recommendation_3_dropdown = os.path.join(BASE_DIR,"media",recommendation_3_dropdown)
                prediction_1_dropdown = os.path.join(BASE_DIR,"media",prediction_1_dropdown)
                prediction_2_dropdown = os.path.join(BASE_DIR,"media",prediction_2_dropdown)
                prediction_3_dropdown = os.path.join(BASE_DIR,"media",prediction_3_dropdown)

                pred_1,pred_2,pred_3,recom_1,recom_2,recom_3 = get_dropdown_values(prediction_1_dropdown,prediction_2_dropdown,prediction_3_dropdown,recommendation_1_dropdown,recommendation_2_dropdown,recommendation_3_dropdown)
        username = request.session['username'] 
        password = request.session['password'] 

        all_users = AD_User.objects.all()
        for user in all_users:
            if user.username == username and user.password == password:
                case_num = request.session['casenum']
                
                user_dict = request.session['user_dict']
                pass_this_user = user_dict[str(case_num)]

        return render(request,'user_ui.html',{'user_dict' : pass_this_user,'pred_1' : pred_1,'pred_2' : pred_2,'pred_3' :pred_3,'recom_1' :recom_1,'recom_2' : recom_2,'recom_3' :recom_3})

    