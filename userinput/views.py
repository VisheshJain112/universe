from django.shortcuts import render
from django.shortcuts import redirect, render
from accounts.models import AD_User
import pandas as pd
from django.core.checks import messages
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse

from django.contrib import messages
from .models import user_validation
import pandas as pd
# Create your views here.
from django.db.models import Q
import numpy as np
import json
from django.template.defaultfilters import register
from pathlib import Path
import os
# Create your views here.
def userinput(request):

    if request.method == "POST":
       
        
        if request.POST.get("next") is not None:
            return redirect('feedback')

            pred_1 = request.POST['pred_1']
            pred_2 = request.POST['pred_2']
            pred_3 = request.POST['pred_3']
            recom_1 = request.POST['recom_1']
            recom_2 = request.POST['recom_2']
            recom_3 = request.POST['recom_3']
            username = request.session['username'] 
            password = request.session['password'] 
            casenum = request.session['casenum']


            user_inputs = user_validation.objects.create(username = username,password = password,case_number = casenum,prediction_1=pred_1,prediction_2=pred_2,prediction_3=pred_3,recommendation_1 = recom_1,recommendation_2 = recom_2,recommendation_3 = recom_3)
            user_inputs.save();
            print("Created")
    
            return redirect('feedback')
        elif request.POST.get("home") is not None:
            return redirect('/index/index_case')
        elif request.POST.get("close") is not None:
            return redirect('/')
        elif request.POST.get("menu") is not None:
            return redirect('/accounts/login')
        else:
            return render(request,'error.html')
    else:
        log_pred = request.session['log_pred']
    
        casenum = request.session['casenum']
        
        dicte = {
        'AI_prediction_1' : log_pred[str(casenum)]["Prediction 1 :"], 
        'AI_prediction_2' : log_pred[str(casenum)]["Prediction 2 :"],
        'AI_prediction_3' : log_pred[str(casenum)]["Prediction 3 :"],
        'AI_recommendation_1' : log_pred[str(casenum)]["Recommendation 1 :"],
        'AI_recommendation_2' : log_pred[str(casenum)]["Recommendation 2 :"],
        'AI_recommendation_3' : log_pred[str(casenum)]["Recommendation 3 :"]}

        def get_value(val):

            val = val.split(',')
            print(val)        

            key = val[0]
            valt = str(val[1])
            valte = str(val[2])
            key_s = key[4:-2]
            value = valt[2:-2]
            if value[0]=='[':
                value = value[1:]
            valuet = valte[2:-2]
            if valuet[0]=='[':
                valuet = valuet[1:]
        
            
            if key_s[0]=='C':
                return str(key_s+" with Relative Confidence  = "+value+"%"+" and with Standard Confidence  = "+valuet+"%")
            else:
                key_s = key[3:-2]
                return str(key_s+" with Relative Confidence  = "+value+"%"+" and with Standard Confidence  = "+valuet+"%")

        for inx,recom in enumerate(dicte['AI_recommendation_1']):
            if inx == 0 :
                recom_h_1 = str(recom)
            elif inx == 1:
                recom_h_2 = str(recom)
            else:
                recom_h_3 = str(recom)
            
            

        

        pred_1_txt =' AI prediction 1 is '+ get_value(str(dicte['AI_prediction_1']))
        pred_2_txt =' AI prediction 2 is '+ get_value(str(dicte['AI_prediction_2']))
        pred_3_txt =' AI prediction 3 is '+ get_value(str(dicte['AI_prediction_3']))
        recom_1_txt =' AI Recommendation 1 is'+ " " + recom_h_1
        recom_2_txt =' AI Recommendation 2 is'+ " " + recom_h_2
        recom_3_txt =' AI Recommendation 3 is'+ " " + recom_h_3

        username = request.session['username'] 
        password = request.session['password'] 

        all_users = AD_User.objects.all()
        for user in all_users:
            if user.username == username and user.password == password:
                case_num = request.session['casenum']
                
                user_dict = request.session['user_dict']
                pass_this_user = user_dict[str(case_num)]

        return render(request,'user_input.html',{'user_dict' : pass_this_user,'pred_1_txt' : pred_1_txt,'pred_2_txt' : pred_2_txt,'pred_3_txt' : pred_3_txt,'recom_1_txt':recom_1_txt,'recom_2_txt':recom_2_txt,'recom_3_txt':recom_3_txt})
