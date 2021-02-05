from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [

    path('watchmoon', views.watchmoon, name="watchmoon"),

]
