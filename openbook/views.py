from django.shortcuts import render

# Create your views here.
def ch1(request):
    content = {'title' : "ch1",
                'content' : """my book """

    }
    return render(request,'openbook.html',{'data' : content})

def ch2(request):
    content = {'title' : "ch2",
                'content' : """my book """

    }
    return render(request,'openbook.html',{'data' : content})

def ch3(request):
    content = {'title' : "ch3",
                'content' : """my book """

    }
    return render(request,'openbook.html',{'data' : content})
def ch4(request):
    content = {'title' : "ch4",
                'content' : """my book """

    }
    return render(request,'openbook.html',{'data' : content})