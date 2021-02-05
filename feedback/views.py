from django.shortcuts import redirect, render
from accounts.models import AD_Admin,AD_User
# Create your views here.
def feedback(request):
    if request.method == "POST":
        if request.POST.get("next") is not None:
            ticket_end = request.session['ticket_end']
            if request.session['casenum'] + 1 <= ticket_end:
                request.session['casenum'] = request.session['casenum'] + 1
                return redirect('/storykey/storykey')
            else:
                return render(request,'error.html')
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
                iframe_code = user.feedback_iframe_code
        username = request.session['username'] 
        password = request.session['password'] 

        all_users = AD_User.objects.all()
        for user in all_users:
            if user.username == username and user.password == password:
                case_num = request.session['casenum']
                
                user_dict = request.session['user_dict']
                pass_this_user = user_dict[str(case_num)]
        if iframe_code!="":
            return render(request,'feedback1.html',{'desc' : iframe_code,'user_dict':pass_this_user})
        else:
            return render(request,'feedback1.html',{'user_dict':pass_this_user})
