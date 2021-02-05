from django.shortcuts import render,redirect

# Create your views here.
def useroptions(request):
    if request.method == "POST":
        if request.POST.get("home") is not None:
            return redirect('/index/index_case')
        elif request.POST.get("close") is not None:
            return redirect('/')
        elif request.POST.get("menu") is not None:
            return redirect('/accounts/login')
        else:
            return render(request,'error.html')
    else:

        return render(request,'useroptions.html')