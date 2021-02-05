from django.shortcuts import render,redirect
from .models import content,demo_book

from pathlib import Path
import os

# Create your views here.
def mainhome(request):
    

    if request.method == 'POST':
        name = request.POST['name']
        countryCode = request.POST['countryCode']
        number = request.POST['number']
        email = request.POST['email']

        booking_info = demo_book.objects.create(name=name,countryCode= countryCode,number=number,email=email)
        booking_info.save();
        print("Created")
  
        return redirect('/')
    else:


        """


        BASE_DIR = Path(__file__).resolve().parent.parent
        for filename in os.listdir(os.path.join(BASE_DIR,'media','pics')):


            fd_img = open(os.path.join(BASE_DIR,'media','pics',filename), 'r', encoding="utf8")
            img = Image.open(fd_img.read())
            img = resizeimage.resize_contain(img, [244, 272])
            img.save(os.path.join(BASE_DIR,'media','pics',filename), img.format)
            fd_img.close()
        """
        cont = content.objects.all()
        return render(request,"homepage.html" , {'cont':cont})
