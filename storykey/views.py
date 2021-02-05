from django.shortcuts import redirect, render
from accounts.models import AD_User,AD_Admin
import pandas as pd
from django.core.checks import messages
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from django.http import HttpResponse

from django.contrib import messages

import pandas as pd
# Create your views here.
from django.db.models import Q
import numpy as np
import json
from django.template.defaultfilters import register
from pathlib import Path
import os

class application_window():

    def __init__(self,p_start_code,p_end_code,test_filepath,prediction_output_filepath,recommendation_filepath):

        self.p_start_code = int(p_start_code)
        self.p_end_code = int(p_end_code)
        self.case_option = 9008
        self.pred_ch_1 = "Null"
        self.pred_ch_2 = "Null"
        self.pred_ch_3 = "Null"
        self.recom_ch_1 = "Null"
        self.recom_ch_2 = "Null"
        self.recom_ch_3 = "Null"
        self.test_sheet = test_filepath
        self.prediction_sheet = prediction_output_filepath
        self.recommendation_sheet = recommendation_filepath 




    def get_recommendation(self,cum_score,score):

        if cum_score < 0 :
            cum_score = 0
        elif cum_score > 5:
            cum_score = 5

        elif 0<=cum_score<=1:
            cum_score = 0
        elif 1<cum_score<=2:
            cum_score = 1
        elif 2<cum_score<=3:
            cum_score = 2
        elif 3<cum_score<=4:
            cum_score = 3
        elif 4<cum_score<5:
            cum_score = 4
        else:
            cum_score = 5
        



        
        
        filepath = self.recommendation_sheet
        df = pd.read_csv(filepath)
        #df_k = df.fillna(" ")
        x = df.iloc[1:,1:].values
        x = x.flatten()

        self.recom_tot_val = []
        for value in x:
            if value!=value:
                pass
            else:
                #print(value)
                self.recom_tot_val.append(value)  

        score_a = df.iloc[6,:]
        score_b = df.iloc[7,:]

        for idx,row in df.iterrows():
            if idx == int(cum_score):
                
                recom = [row['Intepretation-1']] 
                if score=="No Score Defined":
                    recom.append(row['Intepretation-2'])
                    recom.append(row['Intepretation-3'])
                else :
                    if score=='A':
                        recom.append(score_a['Intepretation-2'])
                        recom.append(score_a['Intepretation-3'])

                    else:
                        recom.append(score_b['Intepretation-2'])
                        recom.append(score_b['Intepretation-3'])   

                    
        
        return recom,cum_score,score


    def pad_array(self,d,length):
      #print(len(np.pad(d, (0,(length - len(d)%length)), 'constant')))
      return np.pad(d, (0,(length - len(d)%length)), 'constant')

        
      


    def get_prediction(self,case_num):

        f_pred = self.prediction_sheet
    
        pred = pd.read_csv(f_pred)
        pred_re = pred.loc[pred['Column Reference Code']==case_num]
        
        pred_co = (pred_re['Predcition Codes'].values)[0]
        pred_co = [elt.strip() for elt in pred_co.split(',')]
        pred_co = pred_co[0:3]
        pred_per = (pred_re['Relative Confidence Percentage'].values)[0]
        pred_per = [elt.strip() for elt in pred_per.split(',')]
        pred_per = pred_per[0:3]
        pred_per_s = (pred_re['Standard Confidence Percentage'].values)[0]
        pred_per_s = [elt.strip() for elt in pred_per_s.split(',')]
        pred_per_s = pred_per_s[0:3]
        return pred_co,pred_per,pred_per_s


    def read_output_sheet(self):

        self.total_df = pd.read_excel(self.test_sheet)
        self.score_dict = {}
        df_pred  = pd.read_csv(self.prediction_sheet)
        for inx,rows in df_pred.iterrows():
            self.score_dict[rows['Column Reference Code']] = [rows['Cum-Score'],rows['Score']]


    def get_category_sheet(self):
      
        self.row_lim = len(self.total_df)

        category_sheet = self.total_df['Categories'].values
        self.category_sheet = self.pad_array(category_sheet,self.row_lim+1)
        self.uniqueList = []
        for elem in self.category_sheet:
            if elem!=elem:
                pass
            else:
                self.uniqueList.append(elem)


            

     
      #category_sheet = list(map(int, category_sheet))


    def get_category_value(self):


      return self.category_sheet[self.idx]






 

    def read_cases(self):
        
        self.log_user = {}
        self.log_pred = {}
        for case_num in range(self.p_start_code,self.p_end_code):
            log = {}
            log['case_num'] = case_num
            df_ops = self.total_df[[case_num]]
            df_ops = df_ops.fillna(0)
            df_process = self.total_df.fillna(method='ffill')
            df_attempt = df_ops.where(df_ops == 0, 1)
  
            df_attempt = (df_attempt.iloc[4:,:]).values
            
            df_attempt = df_attempt.flatten()
            score_user = self.score_dict[case_num]
            cum_score,score = score_user[0],score_user[1]
            recommendation = self.get_recommendation(cum_score,score)
            #self.save_recommendation_log(case_num,cum_score,score)

            
            
            
            pred_codes,pred_per,pred_per_s = self.get_prediction(case_num)
            self.log_pred[case_num] = { "Prediction 1 :" : (pred_codes[0],pred_per[0],pred_per_s[0]),
                                   "Prediction 2 :"  : (pred_codes[1],pred_per[1],pred_per_s[1]),
                                   "Prediction 3 :" : (pred_codes[2],pred_per[2],pred_per_s[2]),
                                   "Recommendation 1 :" : recommendation[0],
                                   "Recommendation 2 :" : recommendation[1],
                                   "Recommendation 3 :" : recommendation[2]
                                   

            }

          
            features = df_process.iloc[15:,2].values
            

                    
        
            
            age = df_ops.iloc[3].values
            age = age[0]
            log['age'] = age
            choices = df_ops.iloc[15:,:].values
            feature_choice_dict = {}
            for idx,val in enumerate(choices):
                if val==0:
                    pass
                else:
                    
                    feature_choice_dict[features[idx]] = json.dumps(val[0])
            fet_dict = {}
            for key,val in feature_choice_dict.items():
                if key in ['Info-Features','Codes','Issues','Genetic Parametrs','Feature 37a','Feature 36']:
                    pass
                else:
                    fet_dict[key] = val

            #print(feature_choice_dict)
            log['Feature Mappings'] = fet_dict
            self.idx = 1
            back_category_value = self.get_category_value()

            cat_dict = {}
            cat_dict[back_category_value] = []
            for self.idx,rows in self.total_df.iterrows():
                if self.get_category_value()!=None or self.get_category_value()==self.get_category_value() or self.get_category_value!='nan':
                    if back_category_value == self.get_category_value():
                        dicte= {}
                        if rows['ID'] in fet_dict.keys():
                            dicte[rows['ID']] = fet_dict[rows['ID']]
                            if len(dicte) > 0:
                                if back_category_value!=back_category_value:
                                    pass
                                else:
                                    cat_dict[back_category_value].append(dicte)
                    else:
                        back_category_value = self.get_category_value()
                        if back_category_value!=back_category_value or back_category_value is None:
                            pass
                        else:
                            cat_dict[back_category_value] = []


            self.log_user[case_num] = log
            self.cat_dict = cat_dict
            

    def excute(self):
        self.read_output_sheet()
        self.get_category_sheet()
        self.read_cases()
        
        
        return self.log_user,self.log_pred,self.cat_dict

def fetch_story(filepath,case_num):
    df = pd.read_csv(filepath)
    for inx,rows in df.iterrows():
        if rows['Column Reference Code'] == case_num:
            return rows['Story']


def fetch_data_info(filepath,case_num):
    data_f = pd.read_excel(filepath)


    for inx,rows in data_f.iterrows():
        if rows['Sub-Feature'] == "Jewish":
            val = inx
            break
  
    param_set_1 = data_f.iloc[1:val+1,2:]

    param_set_2 = data_f.iloc[val:,2:]
    cols = param_set_2.iloc[:,1:].columns
    relative_dict = {}
    user_dict = {}
    for col in cols:
        relative_dict[col] = {}
        user_dict[col] = {}




    num_rel = 0
    for inx,row in param_set_2.iterrows():

        if row['Sub-Feature'] == "external factor":
            break

        if row['Sub-Feature'] == "Relative-relation":
            num_rel = num_rel + 1
            
            for idx,col in enumerate(cols):

                relative_dict[col][num_rel]= {}
                relative_dict[col][num_rel]['name'] = row[col]
        elif row['Sub-Feature'] == "Relative-current age/age of death":
            for idx,col in enumerate(cols):
                relative_dict[col][num_rel]['cur_age'] = row[col]
        elif row['Sub-Feature'] == "Relative-bc status":

            for idx,col in enumerate(cols):
                relative_dict[col][num_rel]['bc_status'] = row[col]
        elif row['Sub-Feature'] == "Relative-bilateral":

            for idx,col in enumerate(cols):
                relative_dict[col][num_rel]['bilateral_status'] = row[col]
        elif row['Sub-Feature'] == "Relative-bc status":

            for idx,col in enumerate(cols):
                relative_dict[col][num_rel]['bc_status'] = row[col]
        elif row['Sub-Feature'] == "Relative-bc_onset":

            for idx,col in enumerate(cols):
                relative_dict[col][num_rel]['bc_onset'] = row[col]
        elif row['Sub-Feature'] == "Relative-oc_status":

            for idx,col in enumerate(cols):
                relative_dict[col][num_rel]['oc_status'] = row[col]
        elif row['Sub-Feature'] == "Relative-oc_onset":

            for idx,col in enumerate(cols):
                relative_dict[col][num_rel]['oc_onset'] = row[col]

        elif row['Sub-Feature'] == "Relative-brca_gene":

            for idx,col in enumerate(cols):
                relative_dict[col][num_rel]['brca_gene'] = row[col]

        else:
            pass

    param_set_1 = param_set_1.fillna(0)
    for inx,row in param_set_1.iterrows():
        if row['Sub-Feature'] == "Weight":
            for col in cols:
                user_dict[col]['weight'] = row[col]
        elif row['Sub-Feature'] == "Name":
            for col in cols:
                user_dict[col]['name'] = row[col]
        elif row['Sub-Feature'] == "Accompanied by":
            for col in cols:
                user_dict[col]['accompanied_by'] = row[col]
        elif row['Sub-Feature'] == "Address":
            for col in cols:
                user_dict[col]['address'] = row[col]
        elif row['Sub-Feature'] == "Date":
            for col in cols:
                user_dict[col]['date'] = row[col]
        elif row['Sub-Feature'] == "Age":
            for col in cols:
                user_dict[col]['age'] = row[col]
        elif row['Sub-Feature'] == "Issues":
            for col in cols:
                user_dict[col]['issues'] = row[col]
        elif row['Sub-Feature'] == "Ethinicity":
            for col in cols:
                user_dict[col]['ethinicity'] = row[col]
        elif row['Sub-Feature'] == "Height":
            for col in cols:
                user_dict[col]['height'] = row[col]
        elif row['Sub-Feature'] == "Breast Biopsy":
            for col in cols:
                user_dict[col]['biopsy'] = row[col]
        elif row['Sub-Feature'] == "Parity":
            for col in cols:
                user_dict[col]['parity'] = row[col]
        elif row['Sub-Feature'] == "Breast/Mamographic Density":
            for col in cols:
                user_dict[col]['md'] = row[col]
        elif row['Sub-Feature'] == "Age @ Menarche":
            for col in cols:
                user_dict[col]['menarche'] = row[col]
        elif row['Sub-Feature'] == "Age at first live birth of a child":
            for col in cols:
                user_dict[col]['flb'] = row[col]
        elif row['Sub-Feature'] == "Age @ Menopause":
            for col in cols:
                user_dict[col]['menopause'] = row[col]

        elif row['Sub-Feature'] == "Menopause Status":
            for col in cols:
                user_dict[col]['menopause_status'] = row[col]

        elif row['Sub-Feature'] == "Alcohol Intake":
            for col in cols:
                user_dict[col]['alcohol'] = row[col]
        elif row['Sub-Feature'] == "OC-Pills":
            for col in cols:
                user_dict[col]['oc_pills'] = row[col]
        elif row['Sub-Feature'] == "BRCA Status":
            for col in cols:
                user_dict[col]['brca'] = row[col]
        elif row['Sub-Feature'] == "Ovarian Cancer":
            for col in cols:
                user_dict[col]['oc'] = row[col]
        elif row['Sub-Feature'] == "Ovarian Cancer@Age":
            for col in cols:
                user_dict[col]['oc_age'] = row[col]
        elif row['Sub-Feature'] == "Jewish":
            for col in cols:
                user_dict[col]['jewish'] = row[col]

        elif row['Sub-Feature'] == "HRT Status":
            for col in cols:
                user_dict[col]['hrt_status'] = row[col]
        elif row['Sub-Feature'] == "HRT(if Current) Length of use":
            for col in cols:
                user_dict[col]['hrt_cur_len'] = row[col]
        elif row['Sub-Feature'] == "HRT(if Current) Intended Length of use":
            for col in cols:
                user_dict[col]['hrt_int_len'] = row[col]
        elif row['Sub-Feature'] == "HRT(if Current) Type":
            for col in cols:
                user_dict[col]['hrt_cur_type'] = row[col]
        elif row['Sub-Feature'] == "HRT(if Past) Last used year back":
            for col in cols:
                user_dict[col]['hrt_past_use'] = row[col]
        elif row['Sub-Feature'] == "HRT(if Past) Past Length of use":
            for col in cols:
                user_dict[col]['hrt_past_len'] = row[col]
        elif row['Sub-Feature'] == "HRT(if Past) Type":
            for col in cols:
                user_dict[col]['hrt_past_type'] = row[col]
        else:
            pass
    for col in cols:
        user_dict[col]['FH'] = relative_dict[col]
    return user_dict







def storykey(request):
    username = "admin"
    password = "admin"

    all_users = AD_Admin.objects.all()
    for user in all_users:
        if user.username == username and user.password == password:
            recommendation_sheet = str(user.recommendation_file)
            BASE_DIR = Path(__file__).resolve().parent.parent
            recommendation_sheet = os.path.join(BASE_DIR,"media",recommendation_sheet)

    if request.method == "POST":



        if request.POST.get("extract") is not None:
 
            username = request.session['username'] 
            password = request.session['password'] 

            all_users = AD_User.objects.all()
            for user in all_users:
                if user.username == username and user.password == password:
                    case_num = request.session['casenum']
                    prediction_output = str(user.prediction_output_file) 
                    test_sheet = str(user.data_input_file)
                    BASE_DIR = Path(__file__).resolve().parent.parent
                    test_sheet = os.path.join(BASE_DIR,"media",test_sheet)
                    prediction_output = os.path.join(BASE_DIR,"media",prediction_output)
                    story = fetch_story(prediction_output,case_num)
                    user_dict = fetch_data_info(test_sheet,case_num)
                    request.session['user_dict'] = user_dict
                    pass_this_user = user_dict[case_num]

                    return render(request,'extraction.html',{'story' : story,'user_dict' : pass_this_user,'extract' : "True"})

        elif request.POST.get("home") is not None:
            return redirect('/index/index_case')
        elif request.POST.get("close") is not None:
            return redirect('/')
        elif request.POST.get("menu") is not None:
            return redirect('/accounts/login')

        elif request.POST.get("next") is not None:
 
            username = request.session['username'] 
            password = request.session['password'] 

            all_users = AD_User.objects.all()
            for user in all_users:
                if user.username == username and user.password == password:
                    case_num = request.session['casenum']
                    prediction_output = str(user.prediction_output_file) 
                    test_sheet = str(user.data_input_file)
                    
                    BASE_DIR = Path(__file__).resolve().parent.parent
                    test_sheet = os.path.join(BASE_DIR,"media",test_sheet)
                    prediction_output = os.path.join(BASE_DIR,"media",prediction_output)
                   
  
                    user_dict = fetch_data_info(test_sheet,case_num)
                    request.session['user_dict'] = user_dict
                    app = application_window(p_start_code= int(case_num),p_end_code= int(case_num)+1,test_filepath=test_sheet,prediction_output_filepath=prediction_output,recommendation_filepath=recommendation_sheet)
                    log_user,log_pred,cat_dict = app.excute()
                    request.session['log_pred'] = log_pred
                    pass_this_user = user_dict[case_num]
                  
                    pass_this_log = log_user[int(case_num)]
                    
                    real_cat_dict = {}

                    for cat,value in cat_dict.items():
                        if len(value) > 0:
                            real_cat_dict[cat] = value
                        else:
                            pass
                    
                    pass_this_log = real_cat_dict

                    
                    #pass_this_log = pass_this_log['Feature Mappings']

                    return render(request,'list2.html',{'log_dict' : pass_this_log,'user_dict' : pass_this_user,'next' : "True"})
        elif request.POST.get("f_next") is not None:
            return redirect('user_ui')


        else:
            username = request.session['username'] 
            password = request.session['password'] 

            all_users = AD_User.objects.all()
            for user in all_users:
                if user.username == username and user.password == password:
                    case_num = request.session['casenum']
                    prediction_output = str(user.prediction_output_file) 
                    test_sheet = str(user.data_input_file)
                    BASE_DIR = Path(__file__).resolve().parent.parent
                    test_sheet = os.path.join(BASE_DIR,"media",test_sheet)
                    prediction_output = os.path.join(BASE_DIR,"media",prediction_output)
                    story = fetch_story(prediction_output,case_num)
                    user_dict = fetch_data_info(test_sheet,case_num)
                    request.session['user_dict'] = user_dict
                    pass_this_user = user_dict[case_num]

                    return render(request,'storykey1.html',{'story' : story,'user_dict' : pass_this_user,'extract' : "False"})
            
            
    else:




    
    

    
        username = request.session['username'] 
        password = request.session['password'] 

        all_users = AD_User.objects.all()
        for user in all_users:
            if user.username == username and user.password == password:
                case_num = request.session['casenum']
                prediction_output = str(user.prediction_output_file) 
                test_sheet = str(user.data_input_file)
                BASE_DIR = Path(__file__).resolve().parent.parent
                test_sheet = os.path.join(BASE_DIR,"media",test_sheet)
                prediction_output = os.path.join(BASE_DIR,"media",prediction_output)
                story = fetch_story(prediction_output,case_num)
                user_dict = fetch_data_info(test_sheet,case_num)
                request.session['user_dict'] = user_dict
                pass_this_user = user_dict[case_num]

                return render(request,'storykey1.html',{'story' : story,'user_dict' : pass_this_user,'extract' : "False"})












            else:
                redirect('/')
                    

  





