from django.shortcuts import render,redirect

# Create your views here.
def watchmoon(request):
    if request.method == "POST":
        if request.POST.get("home") is not None:
                return redirect('/world/homescreen')
        else:
            pass
    else:
        return render(request,'watchmoon.html')
def watchsunset(request):
    if request.method == "POST":
        if request.POST.get("home") is not None:
                return redirect('/world/homescreen')
        else:
            pass
    else:
        return render(request,'watchsunset.html')

def timeline(request):
    if request.method == "POST":
        if request.POST.get("home") is not None:
                return redirect('/world/homescreen')
        else:
            pass
    else:
        return render(request,'timeline.html')
    
def watchgallery(request):
    if request.method == "POST":
        if request.POST.get("home") is not None:
                return redirect('/world/homescreen')
        else:
            pass
    else:
        return render(request,'watchgallery.html')

def playbedroom(request):
    if request.method == "POST":
        if request.POST.get("home") is not None:
                return redirect('/world/homescreen')
        else:
            pass
    else:
        return render(request,'playbedroom.html')
def readletters(request):
    if request.method == "POST":
        if request.POST.get("home") is not None:
                return redirect('/world/homescreen')
        else:
            pass
    else:
        return render(request,'readletters.html')
def playmusic(request):
    if request.method == "POST":
        if request.POST.get("home") is not None:
                return redirect('/world/homescreen')
        else:
            pass
    else:
        return render(request,'playmusic.html')