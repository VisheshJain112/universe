from django.shortcuts import render,redirect
from accounts.models import AD_User

def index_case(request):

    if request.method == "POST":
        username = request.session['username'] 
        password = request.session['password'] 
        all_users = AD_User.objects.all()
        for user in all_users:
            if user.username == username and user.password == password:
                print("User Authenticated")

                ticket_start = int(user.start_case_number)
                ticket_end = int(user.end_case_number)
                for case in range(ticket_start,ticket_end+1):


                    if request.POST.get(str(case)) is not None:
                        
                        
                

                        
                        request.session['casenum'] = case
                        return redirect('storykey:storykey')
                    else:
                        print(request.POST)



    else:
        

        username = request.session['username'] 
        password = request.session['password'] 
        all_users = AD_User.objects.all()
        for user in all_users:
            if user.username == username and user.password == password:

                ticket_start = int(user.start_case_number)
                ticket_end = int(user.end_case_number)
                request.session['ticket_start'] = ticket_start
                request.session['ticket_end'] = ticket_end

                return render(request,'index_case.html',{'case_num' : range(ticket_start,ticket_end+1)})


    








# Create your views here.
